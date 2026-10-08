langs = ["pt", "en", "es", "it"]
output_chunks = list()
for lang in langs:
    file_path = f"/home/grassinf/EU-RAG-proj/data/{lang}_data.txt"
    with open(file_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    max_chunk = 600 #chunk limit
    current_size = 0
    current_chunk = list()
    for line in lines:
        if len(line) + current_size > max_chunk:
            output_chunks.append("\n".join(current_chunk))
            overlap = current_chunk[-1]
            if len(overlap) + len(line) <= max_chunk:
                current_chunk = [overlap, line]
                current_size = len(overlap) + len(line)
            else:
                current_chunk = [line]
                current_size = len(line)
        else:
            current_chunk.append(line)
            current_size += len(line)
    output_chunks.append("\n".join(current_chunk))
print(len(output_chunks))

