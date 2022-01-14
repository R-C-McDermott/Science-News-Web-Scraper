"""
Web-scraping project to extract science news from well known reliable websites
By Ryan C. McDermott

so far:
- Able to scrape title and link for article from single website 'Eurekalert'.
- Develop a webpage for the information to be displayed and accessed (Flask or Django).

to-do:
- Scrape from more than one website.
- Construct home page leading to different pages depending on which news website you want.
- Add abstracts to be displayed under each news story.

"""

from flask import Flask, render_template
from webscraper import NewsStories

app = Flask(__name__)


# Initialise news object from webscraper.py and return latest news
def initialise_news_object():
    news_object = NewsStories()
    news_object.set_date()
    return news_object.get_news()


@app.route("/")
def home_page():
    return render_template("index.html", content=news_stories)


if __name__ == "__main__":
    news_stories = initialise_news_object()
    app.run(debug=True)
