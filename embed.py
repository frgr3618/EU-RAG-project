import requests
import numpy as np

url = "http://localhost:11434/api/embed" #ollama connection
#next list to send three requests to the embedding model and compare them with dot.product
input_list= ["qual é o tempo medio de entrega?", "The seller must deliver the goods within 30 days of your purchase", "Pode devolver um artigo em segunda mão no prazo de 14 dias"]
order = {"model": "bge-m3", "input": input_list} 

#reply is a post request to the model
reply = requests.post(url, json=order)
data = reply.json() #convert the JSON reply into dict

#to measure closeness-> dot product -> multiply vectors
"""
To make the dot products in code
"""
pt_en_dot = 0
pt_pt_dot = 0
for x, y in zip(data["embeddings"][0], data["embeddings"][1]): #embeddings is the key in the json
    pt_en_dot += (x*y)
for w, z in zip(data["embeddings"][0], data["embeddings"][2]):
    pt_pt_dot += (w*z)
print(pt_en_dot)
print(pt_pt_dot)

#or in a simpler way
pt_en = np.dot(data["embeddings"][0], data["embeddings"][1])
pt_pt = np.dot(data["embeddings"][0], data["embeddings"][2])
print (pt_en)
print (pt_pt)

"""
Meaning beat language. The English delivery sentence scores about 0.63, the Portuguese returns 
sentence about 0.48. Language can be a bias but the chosen embedding model works multilingually.
The Portuguese question can find an English chunk, if that's where the answer is
"""
