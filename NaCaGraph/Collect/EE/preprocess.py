import os
import glob
from utils import read_json
from utils import sentencize
from utils import build_input_for_ee
from utils import write_input_for_ee
from argparse import ArgumentParser
import time


# Get file paths for all wikinews articles and append *.json at the end.
news_text_path = '../Scrape/wikinews/'
file_paths = glob.glob(news_text_path + "*.json")
print('file_paths:', file_paths, '\n')

def preprocess(file_paths:list[str]):
    """
    Data preprocessing: Take the scraped news articles, i.e. the JSON files under the directory Collect/wikinews/, as inputs, and convert them to txt files as the input of the event extraction. The outputs are written under the input_data/ directory.
    
    Args:
        file_paths:list[str]    List of the paths for all wikinews articles, together with their file names (*.json).
    """
    
    for fp in file_paths:
        print('fp:', fp, '\n')
        start_time = time.time()
        fn = os.path.basename(fp)[:-5]
        articles = read_json(fp)
        articles = build_input_for_ee(articles)
        for aid, art in articles.items():
            output_path = './input_data/' + fn
            print('output_path:', output_path, '\n')
            file = open(output_path + f'/{aid}.txt', 'w')
            file.write(art)
            file.close()
        end_time = time.time()
        print(f'--- Time for preprocessing articles of topic {fn}: %s seconds' % (end_time - start_time))


preprocess(file_paths)
