# The Collect part of the project.

This directory contains following contents:

- input_urls: The input directory containing a txt file.
    - urls.txt: A txt file containing the urls of the webpages to be scraped.
    
- wikinews: The output directory containing the scraped news articles in JSON format.

- scrape.py: The script for scraping news articles from webpage.
             Usage:
                 1. Prepare the input: Write the urls of the webpages to be scraped in the urls.txt file, one url per line.
                 2. Run scrape.py using the following command:
                         python scrape.py -i input_urls/ -o wikinews/
                         
- README.txt: This file.
