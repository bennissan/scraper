import requests
import newspaper
import re

code_words = ["Jew", "Zionist", "Globalist", "Elite", "Rothschild", "\(\(\(.\)\)\)", "Reptilian",
              "New World Order", "Kabbal"]

source_urls = ["http://breitbart.com/", "http://dailycaller.com/", "http://drudgereport.com/",
               "http://www.dailywire.com/", "http://www.nationalreview.com/"]


def main():
    sources = build_sources(source_urls)

    for source in sources:
        url, num_articles, count = scrape(source)
        send_report(url, num_articles, count)


def build_sources(urls):
    sources = []

    papers = [newspaper.build(url, fetch_images=False) for url in urls]
    assert len(urls) == len(papers)

    newspaper.news_pool.set(papers, threads_per_source=10)
    newspaper.news_pool.join()

    for i in range(len(urls)):
        sources.append({"url": urls[i], "articles": papers[i].articles})

    return sources


def scrape(source):
    url = source["url"]
    articles = source["articles"]

    num_articles = len(articles)
    count = 0

    for article in articles:
        article.parse()
        for code_word in code_words:
            count += get_word_count_in_article(code_word, article)

    return url, num_articles, count


def get_word_count_in_article(word, article):
    title_words = re.findall(word, article.title, re.IGNORECASE)
    text_words = re.findall(word, article.text, re.IGNORECASE)

    return len(title_words) + len(text_words)


def send_report(url, num_articles, count):
    report = {"value1": url, "value2": num_articles, "value3": count}
    requests.post("https://maker.ifttt.com/trigger/scraper/with/key/cAb2qiUvSxFnVBTj1dZ7dQ", data=report)


main()
