import requests

url = "http://localhost:11434/api/embed" #ollama connection
order = {"model": "bge-m3", "input": "qual é o tempo medio de entrega?"} 

#reply is a post request to the model
reply = requests.post(url, json=order)
data = reply.json() #convert the JSON reply into dict
#print(data) -> to check which key I need
print(len(data["embeddings"][0]))
print(data["embeddings"][0][:5])

#to measure closeness-> dot product -> multiply vectors
