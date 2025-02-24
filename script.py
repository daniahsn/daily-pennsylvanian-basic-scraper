"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data_point():
    """
    Scrapes the main headline from The Daily Pennsylvanian home page.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    headers = {
        "User-Agent": "cis3500-scraper"
    }

    homepage_url = "https://www.thedp.com"
    req = requests.get(homepage_url, headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")


    
    if not req.ok:
        loguru.logger.warning("Failed to fetch homepage")
        return {"headline": "", "authors": []}

    soup = bs4.BeautifulSoup(req.text, "html.parser")
    target_element = soup.find("a", class_="frontpage-link large-link")

    if target_element is None:
        loguru.logger.warning("No main headline found!")
        return {"headline": "", "authors": []}

    headline = target_element.text.strip()
    article_url = homepage_url + target_element["href"]  # Get full article URL

    loguru.logger.info(f"Headline: {headline}")
    loguru.logger.info(f"Article URL: {article_url}")

    # Request the full article page
    article_req = requests.get(article_url, headers=headers)

    if not article_req.ok:
        loguru.logger.warning("Failed to fetch the article page!")
        return {"headline": headline, "authors": []}

    # Parse article page to find author(s)
    article_soup = bs4.BeautifulSoup(article_req.text, "html.parser")

    # Find the <span class="byline"> and extract all <a class="author-name">
    byline_span = article_soup.find("span", class_="byline")
    
    if byline_span:
        author_elements = byline_span.find_all("a", class_="author-name")
        authors = [author.text.strip() for author in author_elements]
    else:
        authors = []

    loguru.logger.info(f"Authors: {authors}")

    return {"headline": headline, "authors": authors}

if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    #OTHER FUNC
    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
