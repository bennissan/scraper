import requests
from bs4 import BeautifulSoup
import newspaper
import re

sources = [{"name": "Breitbart",         "url": "http://breitbart.com/"},
           {"name": "The Daily Caller",  "url": "http://dailycaller.com/"},
           {"name": "The Drudge Report", "url": "http://drudgereport.com/"}]

codeWords = ["Jew", "Zionist", "Globalist", "Elite", "Rothschild", "\(\(\(.\)\)\)", "Reptilian",
             "New World Order", "Kabbal"]


def sendReport(name, url, count):
    report = {"value1": name, "value2": url, "value3": count}
    requests.post("https://maker.ifttt.com/trigger/scraper/with/key/cAb2qiUvSxFnVBTj1dZ7dQ", data=report)


for source in sources:
    name = source["name"]
    url = source["url"]
    count = 0
    news = newspaper.build(url, memoize_articles=False)

    for article in news.articles[:50]:
        response = requests.get(article.url)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        for codeWord in codeWords:
            count += len(soup.body.find_all(text=re.compile(codeWord, re.IGNORECASE), recursive=True))

    sendReport(name, url, count)