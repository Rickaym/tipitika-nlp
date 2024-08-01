import json
import re

from os import getenv, listdir
from dotenv import load_dotenv
from openai import OpenAI
from typing import Any, TypedDict
from tools import ToolProcessor


complex_dictionary = {}
for i in listdir("../data/dictionaries/complex/en"):
    with open(f"data/dictionaries/complex/en/{i}", "w") as f:
        complex_dictionary[i] = json.load(f)


def strip_html_regex(text):
    # Remove HTML tags
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


class TRelatedContent(TypedDict):
    query: str


class Tools:
    @staticmethod
    def define_term(term: str):
        """
        Get the glossary definition of a pali term.

        term (required): the pali term
        """

        # 1. literal match
        for dict_name, defs in complex_dictionary.items():
            definition = defs.get(term)
            if definition:
                return strip_html_regex(definition)

    @staticmethod
    def search_keyword(keyword: str):
        """
        Get verses containing the keyword.

        keyword (required): the pali/english keyword
        """
        pass

    @staticmethod
    def search_related_content(related_content: TRelatedContent):
        """
        Get verses that relates to the provided text or topic.

        related_content (required): the text/topic to query
        query (required): the query text
        """


load_dotenv()
openai = OpenAI(api_key=getenv("OPENAI_API_KEY"))


def get_response(prompt: str, tool_cls: type):
    tooling = ToolProcessor(tool_cls)

    messages: Any = [{"role": "user", "content": prompt}]
    while True:
        response = openai.chat.completions.create(
            messages=messages, model="gpt-4o", tools=tooling.get_tools()
        )
        if response.choices[0].finish_reason == "tool_calls":
            messages.append(response.choices[0].message)
            messages.extend(
                tooling.process_tool_calls(response.choices[0].message.tool_calls or [])
            )
        else:
            return response.choices[0].message.content


print(get_response("what is the five percepts?", tool_cls=Tools))
