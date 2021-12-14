from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

url_eurek_alert = f"https://www.eurekalert.org/news-releases/browse?view=summaries&date={get_date()}"
url_nature = "https://www.nature.com/latest-news"
url_science = "https://www.science.org/news/all-news"

url_list = [url_eurek_alert, url_nature, url_science]


def get_date():
    year, month, day = datetime.today().strftime('%Y-%m-%d').split("-")
    return f"{month}/{day}/{year}"


def main():
    bs_list = []
    for url in url_list:
        html = urlopen(url)
        bs_list.append(BeautifulSoup(html.read(), 'html.parser'))


if __name__ == "__main__":
    main()