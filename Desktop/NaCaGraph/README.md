# NaCaGraph: Visualizing Event Graph for Natural Catastrophes from News Articles
Text Technology SS2023.

Li Lin, Chong Shen, Xiru Tong

# This directory contains following contents:

- main.py: The main code file for running the whole project. 
           By defult event extraction part is skipped because it should take several hours. Uncomment the corresponding codes to run it instead.

- Collect: The directory containing codes and files of Collect part.
    - EE: The directory containing codes and files regarding event extraction. See README.txt in EE.
    - Scrape: The directory containing codes and files regarding scraping Wikinews webpage. See README.txt in Scrape.

- Prepare: The directory containing codes and files of Prepare part.
    - See README.txt in Prepare.

- Access: The directory containing queries/codes and files of Access part.
    - See README.txt in Access.

                         
- README.txt: This file.


# How to run the whole project:
- STEP1: Change directory to Collect/Scrape/input_urls, open urls.txt
- STEP2: Paste the wikinews website links, one link per line. The existing urls can be used as examples.
(Using the sample urls is recommended. If you want to analyze the news with the topic beyond the existing ones, please uncomment the codes of event extraction in the main.py)
- STEP3: Run main.py to get XML files.
- STEP4: The subsequent steps are explained in README.txt in Access.
