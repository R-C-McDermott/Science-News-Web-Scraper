from bs4 import BeautifulSoup
from datetime import datetime
import requests


class NewsStories:
    def __init__(self):
        self.day = None
        self.month = None
        self.year = None

    # Returns today's date required for latest news in 'Eurek Alert' url
    def set_date(self):
        self.year, self.month, self.day = datetime.today().strftime('%Y-%m-%d').split("-")

    def get_news(self):
        # News website base url and latest news url
        base_url = "https://www.eurekalert.org"
        url_eurek_alert = f"https://www.eurekalert.org/news-releases/" \
                          f"browse?view=titles&date={self.month}/{self.day}/{self.year}"

        r = requests.get(url_eurek_alert)
        html = r.content
        bs = BeautifulSoup(html, 'html.parser')

        # Find all article sections corresponding to individual stories
        articles = bs.find_all('article', class_='post')
        titles, links = [], []

        # Extract title and link for each article section in the html code
        for article in articles:
            title_tags = article.find_all('h2', class_='post_title')
            link_tags = article.find_all('a', href=True)

            titles.append(title_tags)
            links.append([(base_url + link.get('href')) for link in link_tags])

        reform_titles = [title[0].get_text() for title in titles]
        reform_links = [link[0] for link in links]

        # Create dictionary linking titles to links
        news_stories = dict(zip(reform_titles, reform_links))
        return news_stories
