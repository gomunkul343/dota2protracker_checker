from bs4 import BeautifulSoup
from backend.get_from_d2pt import get_db_links, get_browser_headers, get_all_hero_db_links
import random
import time
import requests


class Match:

    def __init__(self, db_link="", replay_id="", match_heroes=None, victory=""):
        self.__db_link = db_link
        self.__replay_id = replay_id
        if match_heroes is None:
            match_heroes = []
        self.__heroes = match_heroes
        self.__victory = victory

    def db_link(self):
        return self.__db_link

    def replay_id(self):
        return self.__replay_id

    def heroes(self):
        return self.__heroes

    def victory(self):
        return self.__victory

    def info(self):
        print(self.replay_id(), self.heroes(), self.victory())

    def __str__(self):
        return self.replay_id()


headers = get_browser_headers()


def get_soup(link):
    response = requests.get(link, headers=headers).content.decode("utf-8")
    su = BeautifulSoup(response, "lxml")
    if su.text.strip() == "Retry later":
        return False
    else:
        return su


def get_replay_id(link):
    return link[33:len(link)]


def get_match_info(soup, link):
    heroes = []
    soup_heroes = soup.find_all("div", {
        "class": "image-container image-container-hero image-container-icon image-container-overlay"})

    for i in soup_heroes:
        heroes.append(i.find("img").get("title"))

    if None in heroes:
        heroes = []
        for i in soup_heroes:
            heroes.append(i.find("img").get("oldtitle"))
    victory = soup.find("div", {"class": "match-show"}).find("div", {"class": "match-result team radiant"}) \
        if (soup.find("div", {"class": "match-show"}).find("div", {"class": "match-result team radiant"}) is not None) \
        else (soup.find("div", {"class": "match-show"}).find("div", {"class": "match-result team dire"}))
    victory = victory.text.split()[0]
    cur_match = Match(link, get_replay_id(link), heroes, victory)
    return cur_match


def human_imitation_1():
    time.sleep(random.uniform(1.5, 5))


def parse():
    db_links = get_db_links()
    print(len(db_links))
    match_id = set()
    missed_links = set()
    miss_count = 0
    Replays = []
    for link in db_links:
        human_imitation_1()
        soup = get_soup(link)
        if not soup:
            missed_links.add(link)
            miss_count += 1
            print(str(miss_count) + " / "+ str(len(db_links)))
            continue
        # human_imitation_2() если сайт банит

        Replays.append(get_match_info(soup, link))
    print(str(miss_count) + " ссылок пропущено")
    if len(missed_links) > 0:
        print(missed_links)
    return Replays
