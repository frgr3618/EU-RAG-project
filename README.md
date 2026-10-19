# EU-RAG-project

A retrieval-augmented generation (RAG) project built step by step, without frameworks, to learn how each part works.

The source text is the EU "Your Europe" page on consumer rights for shopping, in four languages: Portuguese, English, Spanish and Italian. The goal is to answer consumer questions in any of these languages using a small local model, and to compare the answers with and without retrieval.

## Status

Work in progress.

| Step | File | Status |
|---|---|---|
| Baseline: ask the model directly, no retrieval | `baseline.py` | Done |
| Scrape the source page in 4 languages | `scrape.py` | Done |
| Split the text into chunks | `chunk.py` | Done |
| Embeddings (BGE-M3) | `embed.py` | Done |
| Manual search (dot product, top 3) | `search.py` | Done |
| Vector store (Chroma) | | Next |
| Prompt + answer with retrieved chunks | | Planned |

## How it works so far

**baseline.py** sends one question to Llama 3.2 1B through the Ollama API and prints the answer. This is the reference point for the RAG version.

**scrape.py** downloads the page for each language, keeps only the main article, extracts the text of headings, paragraphs and list items, and saves one file per language to `data/{lang}_data.txt`. Each file has 120 lines, and line N has the same content in every language.

**chunk.py** groups neighbouring lines into chunks of at most 600 characters, cutting only between lines and repeating the last line of a chunk at the start of the next one (overlap). Each language is chunked separately, which gives 151 chunks in total. Each chunk is stored as a dict with its text, language, chunk id (for example `pt_5`) and source URL, and the full list is saved to `data/chunks.json`.

**embed.py** is a small test of the embedding model. It embeds a Portuguese question, an English sentence about delivery and a Portuguese sentence about returns, and compares them with the dot product (equal to cosine similarity, since the vectors are normalized). The English delivery sentence scored higher (0.63) than the Portuguese returns sentence (0.48), which shows the multilingual model matches on meaning rather than language.

**search.py** loads the chunks, embeds all of them with BGE-M3 through Ollama in one request, embeds the question, scores every chunk by dot product and prints the top 3. For "qual é o tempo medio de entrega?" the top results contain the rule that the seller must deliver within 30 days.

## Setup

Requirements:

- Python 3.13
- [Ollama](https://ollama.com) running locally, with both models pulled:

  ```
  ollama pull llama3.2:1b
  ollama pull bge-m3
  ```

Create a virtual environment and install the packages:

```
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 numpy
```

## Usage

The `data/` folder is not tracked in git. Create it by running the scraper first:

```
mkdir -p data
python scrape.py
python chunk.py
python search.py
python baseline.py
```

Everything runs on CPU. The first call after starting Ollama can take around 30 seconds while a model loads, and embedding all chunks in `search.py` takes one to three minutes.

## Next steps

- Store the chunk vectors in Chroma, so the chunks are embedded once instead of on every search, and use metadata to filter by language.
- Build the prompt from the retrieved chunks and the question, and get the answer from Llama.
- Later: build a small test set of questions and compare chunking methods.
