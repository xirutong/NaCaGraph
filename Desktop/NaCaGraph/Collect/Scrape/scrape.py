import os
import glob
from tqdm import tqdm
import requests
import re
import json
from argparse import ArgumentParser
import time

from bs4 import BeautifulSoup
# from utils import sentencize
from utils import read_txt
# from utils import CLIMATE_CHANGE, DROUGHT, EARTHQUAKE, FOREST_FIRE, GREENHOUSE, HIGH_TEMPERATURE, WILDFIRE

current_dir = os.path.dirname(os.path.realpath(__file__))


def get_metadata(url: str):
    """
    Scrape the first 100 articles from the webpage for the search results.
    (The number of articles to be scraped is specified in the url.)
    
    Build a mapping from article_id (aid) to the metadata of the article.
    The metadata object is a mapping from "heading" to the news headline, 
    from "link" to the url of the news page, and 
    from "date" to a list [<day>, <month>, <year>].
    
    Args:
        url:str    The url of the webpage for the search results.
        
    Return:
        aid2metadata:dict    A mapping from article_id (aid) to metadata object.
    """
    
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="mw-content-text")

    i = 1  # article serial number
    articles = results.find_all("li", class_="mw-search-result mw-search-result-ns-0")
    aid2metadata = dict()
    for article in articles:
        date = article.find("div", class_="mw-search-result-data")
        rule = r'(\d+,*\d*)\swords'
        the_words = re.findall(rule, date.text)
        # Words of an article used to filter out non-news.
        article_words_num = int("".join(the_words[0].split(',')))
        
        if article_words_num != 0:
            heading = article.find("div", class_="mw-search-result-heading")
            link_loc = heading.find_all("a") # link
            link_url = link_loc[0]["href"]
            rule = r',\s(.+)'  # to get date text
            the_date = re.findall(rule, date.text)

            aid2metadata[i] = dict()
            aid2metadata[i]['heading'] = heading.text
            aid2metadata[i]['link'] = 'https://en.wikinews.org' + link_url
            i += 1
    return aid2metadata


def get_articles_text(aid2metadata): #info is a dic
    aid2articles_text = dict()
    aid2publish_date = dict()
    for aid, article in aid2metadata.items():
        link = article['link']
        print("link:", link)
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        publish_date = _get_publish_date(soup)
        if publish_date != 'None':
            aid2publish_date[aid] = publish_date
            article_content = soup.find("div", class_="mw-parser-output")
            texts_content = article_content.find_all('p', recursive=False)
            sentences_all = []
            for t in texts_content[1:]:
                sentences = t.text.split('\n')[0].strip()
                if sentences != '':
                    sentences_all.append(sentences)
            texts_pure= ' '.join(sentences_all)
            aid2articles_text[aid] = texts_pure
        
    return aid2articles_text, aid2publish_date

def _get_publish_date(soup):
        publish_date = soup.find("strong", class_="published")
        if publish_date is None:
            publish_date = 'None'
        else:
            publish_date = publish_date.text
            publish_date = publish_date.replace(',', '').split(' ')
            publish_date = '-'.join([publish_date[2], publish_date[1], publish_date[3]])
        return publish_date
    
    
def write_file(output_path:str, output_file:dict):
    with open(output_path, 'w') as file:
        json.dump(output_file, file)


def scrape(input_path:str, output_path:str):
    assert input_path[-1] == '/' and output_path[-1] == '/'
    # list of urls
    urls = read_txt(input_path + 'urls.txt')
    
    for i, url in tqdm(enumerate(urls)):
        # topic_id == index(url)+1 in urls
        tid = str(i + 1)
        print("\n\n############ url: ############\n", url, '\n')
        aid2article = get_metadata(url)
        aid2articles_text, aid2publish_date = get_articles_text(aid2article)

        for aid, date in aid2publish_date.items():
            aid2article[aid].update({'date': date})
        
        aid2article_with_date = dict()
        for aid in aid2articles_text:
            article = aid2article[aid]
            article['text'] = aid2articles_text[aid]
            aid_new = tid + '-' + str(aid)
            aid2article_with_date.update({aid_new: article})
        print("length(aid2article):", len(aid2article), 
              "\nlength(aid2articles_text):", len(aid2articles_text), 
              "\nlength(aid2article_with_date):", len(aid2article_with_date), '\n')
        form = url.split('=')[-1].replace('+', '_')
        output_path_file = os.path.join(output_path, f'wikinews_{form}.json')
        write_file(output_path_file, aid2article_with_date)
    


parser = ArgumentParser()
parser.add_argument('-i', '--input_dir', help='path to the input folder (urls of webpages)')
parser.add_argument('-o', '--output_dir', help='path to the output folder (wikinews)')

args = parser.parse_args()

print("Start scraping...")
start_time = time.time()
scrape(input_path=args.input_dir, output_path=args.output_dir)
end_time = time.time()
print("Scraping done!")
print("--- %s seconds ---" % (end_time - start_time))
