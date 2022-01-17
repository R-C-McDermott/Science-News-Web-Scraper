from bs4 import BeautifulSoup
import requests


class NewsStories:
    def __init__(self, base_url, latest_news_url, article_class_tag,
                 article_class_name, title_tag, title_tag_name, link_tag):
        self.base_url = base_url
        self.latest_news_url = latest_news_url
        self.article_class_tag = article_class_tag
        self.article_class_name = article_class_name
        self.title_tag = title_tag
        self.title_tag_name = title_tag_name
        self.link_tag = link_tag

    def get_news(self):
        r = requests.get(self.latest_news_url)
        html = r.content
        bs = BeautifulSoup(html, 'html.parser')

        # Find all article sections corresponding to individual stories
        articles = bs.find_all(self.article_class_tag, class_=self.article_class_name)
        titles, links = [], []

        # Extract title and link for each article section in the html code
        for article in articles:
            title_tags = article.find_all(self.title_tag, class_=self.title_tag_name)
            link_tags = article.find_all(self.link_tag, href=True)

            titles.append(title_tags)
            links.append([(self.base_url + link.get('href')) for link in link_tags])

        reform_titles = [title[0].get_text() for title in titles]
        reform_links = [link[0] for link in links]

        # Create dictionary linking titles to links
        news_stories = dict(zip(reform_titles, reform_links))
        return news_stories
