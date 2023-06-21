import requests
import lxml
from bs4 import BeautifulSoup

def get_pokemon_list(local="uk"):
    link = f"https://www.pokemon.com/{local}/pokedex"

    #get pokedex page as soup
    sess = requests.Session()
    req = sess.get(link)
    soup = BeautifulSoup(req.text, features="lxml")

    #find the Pokedex list on the page
    h2div = soup.find("h2", string="National Pokédex").findNext('ul')
    #get links to every pokemon
    link_list = [entry.get('href') for entry in h2div.find_all("a")]

    return link_list


def get_pokemon_properties(pokedex_link):
    entry_dict = {}
    link = f"https://www.pokemon.com/{pokedex_link}"

    # get pokedex page as soup
    sess = requests.Session()
    req = sess.get(link)
    soup = BeautifulSoup(req.text, features="lxml")

    #get name and pokedex-id
    info = soup.find('div', {'class': "pokedex-pokemon-pagination-title"}).findNext('div')
    entry_dict["Id"] = int(info.findNext().contents[0][1:])  # removes the # infront of the number
    entry_dict["Name"] = info.contents[0].strip()

    #get height and weight
    attributes = soup.find_all('span', {'class': "attribute-title"})
    entry_dict["Height"] = float(attributes[0].findNext().contents[0][:-2])    #removes ' m' at the end
    entry_dict["Weight"] = float(attributes[1].findNext().contents[0][:-3])    #removes ' kg' at the end

    #get gender: female/male booleans
    entry_dict["Male"] = True if attributes[2].findNext().find('i', {'class': "icon icon_male_symbol"}) != None else False
    entry_dict["Female"] = True if attributes[2].findNext().find('i', {'class': "icon icon_female_symbol"}) != None else False

    #get Category
    entry_dict["Category"] = attributes[3].findNext().contents[0].strip()

    #get Abilities
    abilities = attributes[4].findNext()
    entry_dict["Abilities"] = [entry.contents[0].strip() for entry in abilities.findAll('span')]   #all the rest values should be abilities

    #get types
    types = soup.find('div', {'class': "dtm-type"})
    entry_dict["Type"] = [entry.contents[0].strip() for entry in types.findAll('a')]

    #get weaknesses
    weaknesses = soup.find('div', {'class': "dtm-weaknesses"})
    entry_dict["Weaknesses"] = [entry.contents[0].strip() for entry in weaknesses.findAll('span')]

    return entry_dict


def main():
    urls = get_pokemon_list()
    print(urls)
    print(f"Total Pokemon: {len(urls)}")
    print(get_pokemon_properties(urls[871]))

if __name__ == "__main__":
    main()
