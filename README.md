# EU-RAG-project

A retrieval-augmented generation (RAG) project built step by step, without frameworks, to learn how each part works.

The source text is the EU "Your Europe" page on consumer rights for shopping, in four languages: Portuguese, English, Spanish and Italian. The goal is to answer consumer questions in any of these languages using a small local model, and to compare the answers with and without retrieval.

## Status

Work in progress.

| Step | File | Status |
|---|---|---|
| Baseline: ask the model directly, no retrieval | `baseline.py` | Done |
| Scrape the source page in 4 languages | `scrape.py` | Done |
| Split the text into chunks | `chunk.py` | In progress |
| Embeddings (BGE-M3) | | Planned |
| Vector store (Chroma) | | Planned |
| Retrieval + prompt + answer | | Planned |

## How it works so far

**baseline.py** sends one question to Llama 3.2 1B through the Ollama API and prints the answer. This is the reference point for the RAG version.

**scrape.py** downloads the page for each language, keeps only the main article, extracts the text of headings, paragraphs and list items, and saves one file per language to `data/{lang}_data.txt`. Each file has 120 lines, and line N has the same content in every language.

**chunk.py** groups neighbouring lines into chunks of at most 600 characters, cutting only between lines and repeating the last line of a chunk at the start of the next one (overlap). It currently produces 151 chunks across the four languages.

## Setup

Requirements:

- Python 3.13
- [Ollama](https://ollama.com) running locally, with the model pulled:

  ```
  ollama pull llama3.2:1b
  ```

Create a virtual environment and install the packages:

```
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
```

## Usage

The `data/` folder is not tracked in git. Create it by running the scraper first:

```
mkdir -p data
python scrape.py
python chunk.py
python baseline.py
```

The model runs on CPU. The first call after starting Ollama can take around 30 seconds while the model loads.

## Next steps

- Use the Portuguese chunk boundaries for all four languages, so chunk N has the same content in every language.
- Store each chunk with its language, chunk id and source URL.
- Add embeddings, the vector store, and the retrieval step.
- Later: build a small test set of questions and compare chunking methods.
