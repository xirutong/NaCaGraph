import os
import glob
from utils import listdir_nohidden
from argparse import ArgumentParser
import dill as pickle
import time

import spacy
import torch
from OmniEvent.infer import infer
from collections import defaultdict
from tqdm import tqdm



# Load spacy.
nlp = spacy.load("en_core_web_trf")
# nlp = spacy.load("en_core_web_sm")


def predict(input_path:str, output_path:str):
    """
    Event extraction using OmniEvent. An event is defined as a complex structure that contains an event trigger, the event type accompanied with the trigger, the event arguments, and the roles of the arguments.
    
    Args:
        input_path:str    The path for the input data.
        output_path:str   The path for the output data.
    """
    
    input_paths_topic = listdir_nohidden(input_path)
    print('input_paths_topic:', input_paths_topic, '\n')
    
    # Input path: ./input_data/,  Output path: ./output_data/
    assert input_path[-1] == '/' and output_path[-1] == '/'
    # Paths for the folders of news topics.
    input_paths_topic = listdir_nohidden(input_path)
    
    for file_path in tqdm(input_paths_topic): # file_path <==> topic
        
        # file name
        fn = os.path.basename(file_path)
        print('file_name:', fn, '\n')
        
        # List of paths for the input files under each topic.
        input_file_paths = listdir_nohidden(file_path)
        
        # Article files, format: {file_name: text}.
        file_dict_tokenized = defaultdict()
        for ifp in tqdm(input_file_paths):
            aid = ifp.split('/')[-1][:-4]
                
            with open(ifp, 'r') as article:
                text = article.readline()
                tokens = nlp(text)
                sentences = [str(sent).strip() for sent in tokens.sents]        
                file_dict_tokenized[aid] = sentences
                
        file_dict_tokenized = dict(file_dict_tokenized)
        
        # Results of the event extraction.
        ee_results_maven = defaultdict(list)
        print("Start with event extraction.")
        start_time = time.time()
        for aid, sents in tqdm(file_dict_tokenized.items()):
            for sent in sents:
                if len(sent) > 0:
                    ee_results_maven[aid].append(infer(text=sent, schema='maven', task='EE')[0])
        end_time = time.time()
        print("End of event extraction.")
        print("--- %s seconds ---" % (end_time - start_time))
        ee_results_maven = dict(ee_results_maven)
        
        # Write results to a file.
        with open(output_path + f'/{fn}_events.p', 'wb') as file:
            pickle.dump(ee_results_maven, file)
        print(f'--- File {fn}_events.p written. ---\n\n')



parser = ArgumentParser()
parser.add_argument('-i', '--input_dir', help='path to the input folder (input_data)')
parser.add_argument('-o', '--output_dir', help='path to the output folder (output_data)')

args = parser.parse_args()

predict(input_path=args.input_dir, output_path=args.output_dir)
