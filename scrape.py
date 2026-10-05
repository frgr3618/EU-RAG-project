import requests
from bs4 import BeautifulSoup


#pt url
url = "https://europa.eu/youreurope/citizens/consumers/shopping/shopping-consumer-rights/index_pt.htm"


reply = requests.get(url)
data = reply.text
#get request to website
#shows the html content in text
print(len(data))

#parsing the html just retrieved of main article
soup = BeautifulSoup(data, "html.parser")
main_art_box = soup.find(id="main-article")
extract_main = main_art_box.get_text()
#parsed_text= soup.get_text()
#print(extract_main[:2000])
#print(len(extract_main))

#cleaning the parsing
l = main_art_box.find_all(["h2", "h3", "h4", "p", "li"])
final_text = ""
for block in l:
    extract_block = block.get_text() #turns block into text
    splitted = extract_block.split() #-> creates a list of strings
    new_l = " ".join(splitted)
    final_text = final_text + new_l + "\n"
print(final_text[:2000])
print(len(final_text))