import requests
import datetime
import newspaper
import re

code_words = ["Jew", "Zionist", "Globalist", "Elite", "Rothschild", "\(\(\(.\)\)\)", "Reptilian",
             "New World Order", "Kabbal"]

sources = [{"name": "Breitbart",         "url": "http://breitbart.com/"},
           {"name": "The Daily Caller",  "url": "http://dailycaller.com/"},
           {"name": "The Drudge Report", "url": "http://drudgereport.com/"},
           {"name": "The Daily Wire",    "url": "http://www.dailywire.com/"},
           {"name": "National Review",   "url": "http://www.nationalreview.com/"}]

papers = [newspaper.build(source["url"], memoize_articles=False, fetch_images=False) for source in sources]
newspaper.news_pool.set(papers, threads_per_source=10)
newspaper.news_pool.join()

today = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0))


def is_article_from_today(article):
    return article.publish_date == today


def get_word_count_in_article(word, article):
    title_words = re.findall(word, article.title, re.IGNORECASE)
    text_words = re.findall(word, article.text, re.IGNORECASE)

    return len(title_words) + len(text_words)


def send_report(name, url, count):
    report = {"value1": name, "value2": url, "value3": count}
    requests.post("https://maker.ifttt.com/trigger/scraper/with/key/cAb2qiUvSxFnVBTj1dZ7dQ", data=report)


def main():
    for i in range(len(sources)):
        name = sources[i]["name"]
        url = sources[i]["url"]
        count = 0
        articles = papers[i].articles

        for article in articles:
            article.parse()
            if is_article_from_today(article):
                for code_word in code_words:
                    count += get_word_count_in_article(code_word, article)

        send_report(name, url, count)


main()
