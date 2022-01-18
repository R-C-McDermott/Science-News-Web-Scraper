from bs4 import BeautifulSoup
import requests


class NewsStories:
    def __init__(self, base_url, latest_news_url, article_tag,
                 article_class, title_tag, title_class, summary_tag, summary_class):
        self.base_url = base_url
        self.latest_news_url = latest_news_url
        self.article_tag = article_tag
        self.article_class = article_class
        self.title_tag = title_tag
        self.title_class = title_class
        self.summary_tag = summary_tag
        self.summary_class = summary_class

    def get_news(self):
        r = requests.get(self.latest_news_url)
        html = r.content
        bs = BeautifulSoup(html, 'html.parser')

        # Find all article sections corresponding to individual sts
        articles = bs.find_all(self.article_tag, class_=self.article_class)
        titles, links, summaries = [], [], []

        # Extract title and link for each article section in the html code
        for article in articles:
            title_tags = article.find_all(self.title_tag, class_=self.title_class)
            link_tags = article.find_all('a', href=True)
            summary_tags = article.find_all(self.summary_tag, class_=self.summary_class)

            titles.append(title_tags)
            links.append([(self.base_url + link.get('href')) for link in link_tags])
            summaries.append(summary_tags)

        reform_titles = [title[0].get_text() for title in titles]
        reform_links = [link[0] for link in links]

        reform_summaries = []
        for summary in summaries:
            if summary:
                reform_summaries.append(summary[0].get_text())
            else:
                reform_summaries.append('')

        # Form a nested list including links and summaries for each article
        links_and_summaries = [[link, summary] for link, summary in zip(reform_links, reform_summaries)]

        # Create dictionary linking titles to links and summaries
        news_stories = dict(zip(reform_titles, links_and_summaries))
        return news_stories

