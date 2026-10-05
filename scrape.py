import requests
from bs4 import BeautifulSoup


langs = ["en", "pt", "es", "it"]
for lang in langs:
    url = f"https://europa.eu/youreurope/citizens/consumers/shopping/shopping-consumer-rights/index_{lang}.htm"
    reply = requests.get(url)
    data = reply.text
    soup = BeautifulSoup(data, "html.parser") #parsing the html just retrieved of main article
    main_art_box = soup.find(id="main-article") #finds wanted html tag part
    l = main_art_box.find_all(["h2", "h3", "h4", "p", "li"]) #cleaning the parsing
    final_text = ""
    for block in l:
        extract_block = block.get_text() #turns block into text
        splitted = extract_block.split() #-> creates a list of strings
        new_l = " ".join(splitted) # joins them separated by space
        final_text = final_text + new_l + "\n"
    print(f"final text len for {lang} is {len(final_text)}")
    save_file = f"/home/grassinf/EU-RAG-proj/data/{lang}_data.txt"
    with open(save_file, "w", encoding="utf-8") as f:
        f.write(final_text)