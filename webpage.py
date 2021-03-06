"""
Web-scraping project to extract science news from well known reliable websites
By Ryan C. McDermott

so far:
- Developed a webpage for the information to be displayed and accessed (using Flask).
- Can scrape from more than one website.
- Constructed home page with nav-bar leading to different pages depending on which news website you want.
- Abstracts displayed under each news story if they exist.
- Currently works for three individual websites.
to-do:
- Old news stories appended to database
- Comment tab for each news story -> linked to database
- Website login -> linked to database

"""

from flask import Flask, render_template
from webscraper import NewsStories
from datetime import datetime

# sets today's date required for latest news in 'Eurek Alert' url
year, month, day = datetime.today().strftime('%Y-%m-%d').split("-")

app = Flask(__name__)


# Initialise news object from webscraper.py and return latest news
def initialise_eukeralert_news_object():
    news_object = NewsStories(base_url="https://www.eurekalert.org",
                              latest_news_url=f"https://www.eurekalert.org/news-releases/" \
                                              f"browse?view=summaries&date={month}/{day}/{year}",
                              article_tag='article',
                              article_class='post',
                              title_tag='h2',
                              title_class='post_title',
                              summary_tag='p',
                              summary_class='intro',
                              embedded_title=False,
                              link_class=None)
    return news_object.get_news()


def initialise_nature_news_object():
    news_object = NewsStories(base_url="https://www.nature.com",
                              latest_news_url="https://www.nature.com/latest-news",
                              article_tag='li',
                              article_class=['u-flex-row__item u-flex-row__item--span-1',
                                             'c-article-list__item u-flex-list__item cleared'],
                              title_tag='h3',
                              title_class='c-article-item__title mb10',
                              summary_tag='p',
                              summary_class=None,
                              embedded_title=False,
                              link_class=None)
    return news_object.get_news()


def initialise_sciencedotorg_news_object():
    news_object = NewsStories(base_url="https://www.science.org",
                              latest_news_url="https://www.science.org/news/all-news",
                              article_tag='article',
                              article_class='card-do',
                              title_tag='a',
                              title_class='title',
                              summary_tag='div',
                              summary_class='card-body text-darker-gray',
                              embedded_title=True,
                              link_class='text-reset animation-underline')
    return news_object.get_news()


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/eurekalert")
def eurekalert_page():
    news_stories = initialise_eukeralert_news_object()
    return render_template("eurekalert.html", content=news_stories)


@app.route("/nature")
def nature_page():
    news_stories = initialise_nature_news_object()
    return render_template("nature.html", content=news_stories)


@app.route("/scienceorg")
def scienceorg_page():
    news_stories = initialise_sciencedotorg_news_object()
    return render_template("science.html", content=news_stories)


if __name__ == "__main__":
    app.run(debug=True)
