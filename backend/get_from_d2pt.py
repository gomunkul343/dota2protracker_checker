import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_browser_headers():
    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': "https://www.dotabuff.com/matches"
    }
    return headers


def get_db_links():
    links = set()
    doc = requests.get("https://dota2protracker.com").content.decode("utf-8")
    soup = BeautifulSoup(doc, "lxml")
    db_a = soup.find_all("a", {"class": "info dotabuff"})
    for link in db_a:
        links.add(link.get("href"))
    return links


def get_all_heroes():
    doc = requests.get("https://www.dotabuff.com/heroes", headers=get_browser_headers()).content.decode("utf-8")
    soup = BeautifulSoup(doc, "lxml")
    all_heroes = soup.find_all("div", {"class": "name"})
    dota_heroes = []
    for i in all_heroes:
        dota_heroes.append(i.text)
    return dota_heroes


def make_url(hero_name):
    url = "https://dota2protracker.com/hero/"
    return url + hero_name.replace(" ", "%20") + "#"


def get_all_heroes_url():
    all_heroes = get_all_heroes()
    all_heroes_url = []
    for i in all_heroes:
        all_heroes_url.append(make_url(i))
    return all_heroes_url


def get_db_hero_links(hero_name):
    links = set()
    res = requests.get(make_url(hero_name)).content.decode("utf-8")
    su = BeautifulSoup(res, "lxml")
    db_a = su.find_all("a", {"class": "info dotabuff"})
    for link in db_a:
        links.add(link.get("href"))
    return links


def get_all_hero_db_links():
    links = set()
    heroes = get_all_heroes()
    for name in heroes:
        links.update(get_db_hero_links(name))
    return links


if __name__ == "__main__":
    heroes = get_all_heroes()
    heroes.sort(key=len, reverse=True)
    print(heroes)
    k = 0
    for i in range(5):
        k += len(heroes[i])
        k += 1
    print(k-1)
    print(len(get_all_hero_db_links()))