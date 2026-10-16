import json

#build a list of dicts, each corresponding to a chunk 
#dict struct {"text" : chunk, "lang" : lang, "chunk_id" : lang_chunk, "source" : url}
langs = ["pt", "en", "es", "it"]
output_chunks = list()
for lang in langs:
    file_path = f"/home/grassinf/EU-RAG-proj/data/{lang}_data.txt"
    with open(file_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    url = f"https://europa.eu/youreurope/citizens/consumers/shopping/shopping-consumer-rights/index_{lang}.htm"
    max_chunk = 600 #chunk limit
    current_size = 0 #chars in each chunk
    counter = 0 #for chunk_id 
    current_chunk = list()
    for line in lines:
        if len(line) + current_size > max_chunk: #when this, close the chunk
            chunk_id = f"{lang}_{counter}" # value for the dict
            counter += 1
            output_chunks.append({"text":"\n".join(current_chunk), "lang":lang, "chunk_id":chunk_id, "source":url})
            overlap = current_chunk[-1]
            if len(overlap) + len(line) <= max_chunk: #if the overlap still fits, keep it
                current_chunk = [overlap, line]
                current_size = len(overlap) + len(line)
            else: #start with teh line alone
                current_chunk = [line]
                current_size = len(line)
        else: #add lineto current chunk
            current_chunk.append(line)
            current_size += len(line)
    # save the last chunk
    chunk_id = f"{lang}_{counter}"
    output_chunks.append({"text":"\n".join(current_chunk), "lang":lang, "chunk_id":chunk_id, "source":url})
print(len(output_chunks))
with open("/home/grassinf/EU-RAG-proj/data/chunks.json", "w", encoding="utf-8") as output_file:
    json.dump(output_chunks, output_file, ensure_ascii=False, indent=2)

