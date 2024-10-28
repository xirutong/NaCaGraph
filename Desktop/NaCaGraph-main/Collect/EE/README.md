# The event extraction pipeline of this project.

This directory contains following contents:

- input_data: The input directory for the event extractor.
    - wikinews_*: Directories that contains news articles of each category (i.e. topic), 
                  e.g. wikinews_wildfire means this directory contains all the articles of the category(topic) "wildfire".
        - *.txt: News articles files. Each file has the article_id (aid) of the article it helds as its file name, 
                 e.g. 3-1.txt means this file contains the first article of the third category(topic).
                 
- output_data: The output directory which contains the results of the event extraction.
    - wikinews_*.p: The results of the event extraction of a category, saved as a binary .p file.
    - check_results.ipynb: The code for checking the results.
    
- preprocess.py: The implementation of the data preprocessing. This component takes the scraped news articles, i.e. the JSON files under the directory Collect/wikinews/, as inputs, and converts them to txt files as the input of the event extraction. The outputs are saved under the input_data/ directory.
                 Usage:
                     1. Make sure the JSON files of the extracted news articles are under the directory Collect/wikinews/.
                     2. Run the following command:
                         python preprocess.py

- predict.py: The implementation of the event extraction. We use OmniEvent as our event extraction pipeline. It takes the txt files under the directory input_data/wikinews_*/*.txt as inputs and saves the outputs under the directory output_data/ with file names "wikinews_<cateogory>_events.p".
              Usage:
                  1. Prepare the input: Create a directory with the name "wikinews_<category>", where <category> is the category (i.e. topic) name of the articles. Put all the articles (.txt files) of this category under this directory.
                  2. Run predict.py using the following command:
                      python predict.py -i input_data/ -o output_data/
                      
- utils.py: Auxillary functions for the preprocessing and the event extraction.

- README.txt: This file.
