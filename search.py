import json
import requests
import numpy as np

#loop over the chunks and append "text" to feed to embedding model
with open("/home/grassinf/EU-RAG-proj/data/chunks.json", encoding="utf-8") as chunk_file:
    data = json.load(chunk_file)
texts = list()
for chunk in data:
    texts.append(chunk["text"])

#embed the chunks
url = "http://localhost:11434/api/embed" #ollama connection
order = {"model": "bge-m3", "input": texts}
reply = requests.post(url, json=order)
chunk_reply = reply.json()
chunk_vectors = chunk_reply["embeddings"]

#embed question
order = {"model": "bge-m3", "input": "qual é o tempo medio de entrega?"}
reply_question = requests.post(url, json=order)
question = reply_question.json()
question_vector = question["embeddings"][0]

print(len(chunk_vectors))       # 151
print(len(chunk_vectors[0]))    # 1024
print(len(question_vector))     # 1024

#data holds list of 151 chunk dicts, each with text, lang, chunk_id and source
#zip data and chunk_vectors so you save tuples with id number and dot.prod against question
results = list()
for chunk, vector in zip(data, chunk_vectors): 
    score = np.dot(question_vector, vector)
    scores = (score, chunk["chunk_id"])
    results.append(scores)
results.sort(reverse=True)
print(results[:3])