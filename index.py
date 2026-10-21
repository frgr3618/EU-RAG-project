import json
import requests
import chromadb

"""
Load the chunks from chunks.json, and prepare the data for chromdb the way it needs it:
4 parts in their on lists: ids, documents, metadata, embeddings.
ids -> chunk["chunk_id]
documents -> chunk["text]
metadata -> dict with lang and source
embeddings -> embeddings of the texts of the chunks

After this, populate the vector database with chroma

Run the index only if need to change the chunking, if the docs change, or we change model.
On every query, only the question gets embedded, the rest lives in the DB
"""

#prepare "documents", "ids" and "metadata"
with open("/home/grassinf/EU-RAG-proj/data/chunks.json", encoding="utf-8") as chunk_file:
    data = json.load(chunk_file)
texts = list()
ids = list()
metadata = list()
#print(data)
for chunk in data:
    texts.append(chunk["text"])
    ids.append(chunk["chunk_id"])
    meta_dict = {"lang" : chunk["lang"], "source" : chunk["source"]}
    metadata.append(meta_dict)



#embed all chunk texts with BGE-M3 in one request to make "embeddings"
url = "http://localhost:11434/api/embed" #ollama connection
order = {"model": "bge-m3", "input": texts}
reply = requests.post(url, json=order)
chunk_vectors = reply.json()["embeddings"]

#open the chroma vector database and the collection = a table
client = chromadb.PersistentClient(path="/home/grassinf/EU-RAG-proj/chroma_db")
collection = client.get_or_create_collection(
    name="eu_consumer_rights",
    embedding_function=None,                      #no default model, vectors come from bgem3
    configuration={"hnsw": {"space": "cosine"}},  #cosine distance = 1-dot product
)

#store everything created and populate database
#upsert = update ids that exist, add new ones (no duplicates on re-run)
collection.upsert(ids=ids, embeddings=chunk_vectors, documents=texts, metadatas=metadata)
print(f"Indexed {collection.count()} chunks into chroma_db")


"""
Three ways to write the chunks into the collection:
add -> adds ids that dont exist yet.
    Problem: if an id already exists, it is silently ignored,
    so after rechunking the old text and vector stay in the DB

upsert -> update + insert: updates ids that exist, adds new ones.
    No duplicates when index.py runs again
    Problem: only touches the ids it is given. If new chunking makes fewer
    chunks (ex. 140 instead of 151), the old leftover ids stay in the DB

delete + rebuild -> delete the whole collection, then add everything from scratch
    Always clean, best for the chunking experiments later.
    Problem: deleting a collection that doesn't exist yet (first run) raises an error

    
On top of this, I chose cosine instead of the default squared euclidean distance (chroma default)
Ollama bge3m vectors are normalised to length 1. If u change model, the l2 would be 
affected by vector length, cosine wont and cosine is usually the standard for text    
"""