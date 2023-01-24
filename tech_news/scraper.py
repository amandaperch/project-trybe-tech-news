import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url, wait=1):
    time.sleep(wait)
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=wait
        )
        response.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)
    link = selector.css('a.cs-overlay-link::attr(href)').getall()
    return link


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next = selector.css('a.next::attr(href)').get()
    return next if next else None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)

    news = {
        'url': selector.css("link[rel='canonical']::attr(href)").get(),
        'title': selector.css(".entry-title::text").get().strip(),
        'timestamp': selector.css("li.meta-date::text").get(),
        'writer': selector.css(".author a::text").get(),
        'comments_count': selector.css(".post-comments-simple h5::text").get()
        or 0,
        'summary': selector.css(".entry-content p").xpath("string()").get()
        .strip(),
        'tags': selector.css(".post-tags a *::text").getall(),
        'category': selector.css(".meta-category .label::text").get(),
    }

    return news

# {
#   "url": "https://blog.betrybe.com/novidades/noticia-bacana",
#   "title": "Notícia bacana",
#   "timestamp": "04/04/2021",
#   "writer": "Eu",
#   "comments_count": 4,
#   "summary": "Algo muito bacana aconteceu",
#   "tags": ["Tecnologia", "Esportes"],
#   "category": "Ferramentas",
# }


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com/"
    news = []

    while len(news) < amount:
        html = fetch(url)
        links = scrape_updates(html)
        for link in links:
            if len(news) < amount:
                news.append(scrape_news(fetch(link)))
        url = scrape_next_page_link(html)
        if not url:
            break
    create_news(news)
    return news
