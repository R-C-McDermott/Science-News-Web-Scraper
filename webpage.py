"""
Web-scraping project to extract science news from well known reliable websites
By Ryan C. McDermott

so far:
- Developed a webpage for the information to be displayed and accessed (using Flask).
- Can scrape from more than one website.
- Constructed home page with nav-bar leading to different pages depending on which news website you want.

to-do:
- Add abstracts to be displayed under each news story.

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
                                              f"browse?view=titles&date={month}/{day}/{year}",
                              article_class_tag='article',
                              article_class_name='post',
                              title_tag='h2',
                              title_tag_name='post_title',
                              link_tag='a')
    return news_object.get_news()


def initialise_nature_news_object():
    news_object = NewsStories(base_url="https://www.nature.com",
                              latest_news_url="https://www.nature.com/latest-news",
                              article_class_tag='li',
                              article_class_name=['u-flex-row__item u-flex-row__item--span-1',
                                                  'c-article-list__item u-flex-list__item cleared'],
                              title_tag='h3',
                              title_tag_name='c-article-item__title mb10',
                              link_tag='a')
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


if __name__ == "__main__":
    app.run(debug=True)
