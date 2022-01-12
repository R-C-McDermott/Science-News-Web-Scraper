"""
Web-scraping project to extract science news from well known reliable websites

so far:
- Able to scrape title and link for article from single website 'Eurekalert'

to-do:
- Scrape from more than one website
- Develop a webpage for the information to be displayed and accessed (Flask or Django)

"""

from bs4 import BeautifulSoup
from datetime import datetime
import requests


# Returns today's date required for latest news in 'Eurek Alert' url
def get_date():
    year, month, day = datetime.today().strftime('%Y-%m-%d').split("-")
    return f"{month}/{day}/{year}"


# News website url
base_url = "https://www.eurekalert.org"
url_eurek_alert = f"https://www.eurekalert.org/news-releases/browse?view=titles&date={get_date()}"


def main():
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
    print(news_stories)

if __name__ == "__main__":
    main()