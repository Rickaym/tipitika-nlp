import inspect
import json

from itertools import chain
from typing import Literal, get_args, Union, TypedDict
from openai.types.chat import ChatCompletionMessageToolCall


def parse_params(func, parameters: list[str]):
    required = []
    lines = list(
        z.replace("(required)", "").strip()
        for z in chain.from_iterable(l.split("\n") for l in func.__doc__.split(":"))
        if z.strip()
        # append to required if the param is required
        and not (
            "(required)" in str(z)
            and required.append(z.replace("(required)", "").strip())
        )
    )

    params_desc = {lines[1:][i]: lines[1:][i + 1] for i in range(0, len(lines[1:]), 2)}

    if not all(p in params_desc.keys() for p in parameters):
        raise Exception(
            f"Missing description the params '{parameters}' in {func.__name__}"
        )

    return {"function": lines[0], **params_desc}, required


type_map = {int: "integer", str: "string", bool: "boolean"}


def get_literal_strings(annotation):
    if hasattr(annotation, "__origin__") and annotation.__origin__ is Union:
        union_args = get_args(annotation)

        literal_strings = []
        for arg in union_args:
            if hasattr(arg, "__origin__") and arg.__origin__ is Literal:
                literal_strings.extend(get_args(arg))

        return literal_strings

    return []


def is_union_type(annotation):
    return hasattr(annotation, "__origin__") and annotation.__origin__ is Union


def is_typed_dict_class(cls) -> bool:
    # Check if the class has the required TypedDict attributes
    return (
        isinstance(cls, type)
        and hasattr(cls, "__annotations__")
        and (TypedDict in cls.__bases__ or TypedDict in cls.__orig_bases__)
    )


def get_type(annotation):
    instant_type = type_map.get(annotation)
    if instant_type:
        return instant_type

    if is_union_type(annotation):
        return "string"

    if is_typed_dict_class(annotation):
        return "object"

    raise Exception(f"Unknown type {annotation}")


def get_typed_dict_properties(annotation, descs):
    schema = {}
    type_hints = annotation.__annotations__
    for key, py_type in type_hints.items():
        schema[key] = {"type": get_type(py_type), "description": descs[key]}

    return schema


class ToolProcessor:
    def __init__(self, cls: type) -> None:
        self.tool_cls = cls

    def get_tools(self):
        tool_funcs = [
            f for f in self.tool_cls.__dict__.values() if isinstance(f, staticmethod)
        ]

        definitions = []

        for f in tool_funcs:
            params = inspect.signature(f).parameters
            descs, required = parse_params(f, [p for p in params.keys()])

            definitions.append(
                {
                    "type": "function",
                    "function": {
                        "name": f.__name__,
                        "description": descs["function"],
                        "parameters": {
                            "type": "object",
                            "properties": {
                                k: {
                                    "type": (type := get_type(v.annotation)),
                                    "description": descs[k],
                                    **(
                                        {"enum": get_literal_strings(v.annotation)}
                                        if is_union_type(v.annotation)
                                        else {}
                                    ),
                                    **(
                                        {
                                            "properties": get_typed_dict_properties(
                                                v.annotation, descs
                                            )
                                        }
                                        if type == "object"
                                        else {}
                                    ),
                                }
                                for k, v in params.items()
                            },
                            "required": required,
                        },
                    },
                }
            )

        return definitions

    def process_tool_calls(self, tool_calls: list[ChatCompletionMessageToolCall]):
        messages = []

        for call in tool_calls:
            tool_call_id = call.id
            tool_function_name = call.function.name
            tool_query_string = json.loads(call.function.arguments)

            func = getattr(self.tool_cls, tool_function_name)
            results = func(**tool_query_string)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": tool_function_name,
                    "content": results,
                }
            )
        return messages
