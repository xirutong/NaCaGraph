# import space
import subprocess
import os

# STEP 1 COLLECT: Scrape the websites in urls.txt and output the results to json files.
command = ['python', 'Collect/Scrape/scrape.py', '-i', 'Collect/Scrape/input_urls/', '-o', 'Collect/Scrape/wikinews/']
subprocess.run(command, check=True)
print('Scraping results saved. Collect procedure done.')

# STEP 2 EVENTS EXTRACTION: Extract events and output the results to p files.
# NOTICE: this step is by default skipped and pregenerated data are used, because it should take several hours.
print('Events extraction started...')
os.chdir('Collect/EE/')
###command = ['python', 'preprocess.py']
###subprocess.run(command, check=True)
print("Events extracted and saved.")

# STEP 3 PREPARE: Preprocess p files and turn it into XMLs.
os.chdir('../../Prepare/')
command = ['python', 'events2xml.py']
subprocess.run(command, check=True)
print("All XML files saved. Prepare procedure done.")

# STEP 4 ACCESS: This part is done on the Neo4j website, please check Access folder for more information.
