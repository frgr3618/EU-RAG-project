import requests

#host connection to ollama
url = "http://localhost:11434/api/generate"
#order is a dict where you state model question and kind of output, false means all at once, 
#true means in tokens, this is my request to the llm
order = {"model": "llama3.2:1b", "prompt": "qual é o tempo medio de entrega?", "stream": False} 

#reply is a post request to the model
reply = requests.post(url, json=order)
data = reply.json() #convert the JSON reply into a Python dict
#print(data) -> to check which key I need
print(data["response"]) #print the value of rhe key u want from the json