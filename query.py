import requests
import chromadb

#connect to the db
client = chromadb.PersistentClient(path="/home/grassinf/EU-RAG-proj/chroma_db")
#get the collection (the table)
collection = client.get_collection(name="eu_consumer_rights", embedding_function=None)


#embed question
url = "http://localhost:11434/api/embed"
order = {"model": "bge-m3", "input": "I never received my order"}
reply_question = requests.post(url, json=order)
question = reply_question.json()
question_vector = question["embeddings"][0]

#search the database and find the 3 most likely matches
result = collection.query(query_embeddings=[question_vector], n_results=3)

#every field comes back as a list of lists based on the number of questions
#1 question -> look for position [0]

for ids, distance in zip(result["ids"][0], result["distances"][0]):
    print(ids, distance) #chunk number and its score
