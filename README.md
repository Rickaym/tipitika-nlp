<p align="center">
  <h3 align="center">Tipitika NLP</h3>
  
  <a href="https://tp-recall.pyaesonemyo.com/"><strong>See the Demo »</strong></a>
  </p>
</p>
<!-- Body -->
The Tipitika NLP project aims to create a set of NLP tools to help in the understanding and text searching of the English Tipitika. For those uninitiated, the Tipitika (ပိဋကတ် သုံးပုံ) is a compilation of Buddhist sacred scriptures and doctrinal teachings. It is composed of three main categories of texts that make up the Buddhist canon: the Sutta Piṭaka, the Vinaya Piṭaka, and the Abhidhamma Piṭaka. The English Tipitika is a highly esteemed translation from various indo-aryan and austroasiatic scriptures of the Tipitika.

## Data

1. The Tipitika (Sutta Central)
2. Introduction To Pali - Third Edition (A.K. Warder)

## Roadmap

### 1. Abhidhamma Search

The Abhidamma is composed of 7 books. Each book is divided into parts/chapters which are further separated by titles. The basket has a unique style amongst the Tipitika, it presents the teachings in a systematic and detailed manner, breaking down the components, defining and classifying them. It does not contain narrative stories, parables, or biographical elements. Its focus is on abstract and technical discussions. However, the Kathāvatthu is one exception to this style. It contains a large amount of debates on questions of doctrine, between the Theravada school and other schools.

**Embedding Strategy:**

1. Divide the Abhidhamma into its separate verses
2. Split the verses that exceeds the chunk token limit
3. Each document is attached with the metadata
   - Book name
   - Title
   - Subtitle
   - Whole Content
   - Citation Text and Url

**Retrival Strategy:**

1. Setup chroma-db using the `all-minilm-l6-v2` embedding function
2. Perform dense retrival with the query

Additionally, we will perform a dictionary search on the containing Pali words and include them as part of the results. We will return the top 3 chunks from the Abhidamma that pertains to the user's query and its associated dictionary definitions.

### 2. Abhidhamma RAG v1c

On top of the retrieval system from v1. The minor version v1c intends to pipeline this to Chat GPT4o as tool functions.

## Author's Tradition

As a burmese born Buddhist, I grew up ensconced in the Theravada tradition, and I have always had the deepest respect for the tradition. It is still the tradition that I practice today. Initially, I was not aware of the existence of other Buddhist traditions until it was about my last year of highschool, therefore my knowledge on the differences are very little. That being said, I have taken a purely analytical approach, with adherence to the lay Buddhist ethics. I do not appeal to any specific traditions of buddhism or nor do I include any augmentation or interpretation of the Buddhist religion that are my own. I understand that there are some concerns within the Buddhist on the matter of A.I., particularly generative A.I, therefore, I have made the purpose of this project not to generate additional content based/trained on the Tipitika, but to utilize and present the Tipitika accurately, free of interpretation and evaluation.

Made with <3
