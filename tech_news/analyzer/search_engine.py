from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    title = search_news({'title': {"$regex": title, "$options": 'i'}})
    return [(titles['title'], titles['url']) for titles in title]


# [
#   ("Título1_aqui", "url1_aqui"),
#   ("Título2_aqui", "url2_aqui"),
#   ("Título3_aqui", "url3_aqui"),
# ]

# Requisito 7
def search_by_date(date):
    try:
        format_date = datetime.fromisoformat(date).strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError('Data inválida')
    else:
        news = search_news({'timestamp': format_date})
    return [(new['title'], new['url']) for new in news]

# formato da data tem que ser AAAA-mm-dd


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
