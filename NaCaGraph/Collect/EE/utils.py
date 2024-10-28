import os
import glob
import json
import dill as pickle
from tqdm import tqdm
import time

import spacy
import spacy_transformers

current_dir = os.path.dirname(os.path.realpath(__file__))


def read_json(path:str):
    """
    Read a JSON file.
    
    Args:
        path:str    The path for the JSON file
    """
    
    with open(path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    data = data[0]
    return data


def sentencize(text:str, model="en_core_web_sm"):
    """
    Split a long text containing multiple sentences to a list of sentences.
    
    Args:
        text:str    The text for with the sentences to be split.
        model       The model of spacy, default: "en_core_web_sm".
        
    Return:
        sentences:list[str]    List of sentences split from the input text.
    """
    
    # Load spacy.
    if model == "en_core_web_sm":
        nlp = spacy.load("en_core_web_trf")
    elif model == "en_core_web_trf":
        nlp = spacy.load("en_core_web_trf")
    else:
        raise ValueError("Invalid Argument!")
    
    text = ''.join(text.strip().split('\n'))
    tokens = nlp(text)
    sentences = [str(text) for text in tokens.sents]
    return sentences


def build_input_for_ee(articles:dict):
    """
    Add a stop '.' to the end of the headline sentence.
    Split the sentences in the text.
    Concatenate the news headline with the main text of an article.
    
    Args:
        articles:dict    The mapping from article_id (aid) to the article object which is again a mapping from some tags to the corresponding contents.
        
    Return:
        articles:dict    The mapping from article_id (aid) to the processed article object.
    """
    
    for aid, art in articles.items():
        # Add a stop '.' at the end of the heading of the article.
        art['heading'] = art['heading'][:-1] + "."  # the news heading sentence (str)
        text = art['text']  # the news main text (str)
        print("aid:", aid)
#         print("art[heading]:", art['heading'])
        # Split sentences using spacy.
        sentences = sentencize(text)
#         print('sentences:', sentences, '\n')
        sentences = [art['heading']] + sentences
        articles[aid] = ' '.join(sentences)
        print('articles[aid]:\n', articles[aid], '\n')
    print("build_input_for_ee: Done!")
    return articles
    
    
def write_input_for_ee(articles:dict, output_path:str):
    """
    Write the input file for the event extraction.
    
    Args:
        articles:dict    The mapping from article_id (aid) to the article object.
        output_path:str  The path for the output file.
    """
    
    for aid, art in articles.items():
        file = open(output_path + f'{aid}.txt', 'w')
#         inp = art['heading'] + ' ' + art['text']
        inp = art
        file.write(inp)
        file.close()
        

def listdir_nohidden(path:str):
    """
    Get the names of all non-hidden files under the given path.
    
    Args:
        path:str    The path under wich the names of the files contained are to be listed.
        
    Return:
        A list of names of all non-hidden files under the given path.
    """
    
    return glob.glob(os.path.join(path, '*'))
        
        
        
        
        
        
        
        
        
