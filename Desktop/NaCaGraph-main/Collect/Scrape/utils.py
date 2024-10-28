import os
import glob
import spacy
import spacy_transformers


def sentencize(text:str, model="en_core_web_sm"):
    # Load spacy.
    if model == "en_core_web_sm":
        nlp = spacy.load("en_core_web_trf")
    elif model == "en_core_web_trf":
        nlp = spacy.load("en_core_web_trf")
    else:
        raise ValueError("Invalid Argument!")
    
    text = ''.join(text.split('\n'))
    tokens = nlp(text)
    sentences = [str(text) for text in tokens.sents]
    
    return sentences


def read_all_txt(path:str):
    assert path[-1] == '/'
    file_paths = glob.glob(path + "*.txt")
    data = []
    for fp in file_paths:
        fn = os.path.basename(fp)
        print(fn)
        with open(path + fn, 'r') as file:
            for line in file.readlines():
                line = line.split('\n')[0]
                data.append(line)
        return data
    
    
    
def read_txt(filename:str):
    """
    Read a single txt file.
    """
    assert filename[-4:] == '.txt'
    data = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = line.split('\n')[0]
            data.append(line)
    return data
    
    
    
    
    