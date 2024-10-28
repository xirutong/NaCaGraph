# import space
import dill as pickle
import json
from dict2xml import dict2xml
import re
import os

dir_path = r'..\Collect\Scrape\wikinews'
for filename in os.listdir(dir_path):
    # STEP 1: determine the topic
    topic = filename.replace('wikinews_', '').replace('.json', '')

    # STEP 2: read in the ee results p file and save it as a dictionary
    ee_dict = pickle.load(open(fr'..\Collect\EE\output_data\wikinews_{topic}_events.p', 'rb'))
    result_dict = {key: value for key, value in ee_dict.items() if int(key.split('-')[1]) <= 80}  # limit the number of key&value pairs

    # STEP 3: preprocess dictionary to conform to the XML structure
    # remove redundant items
    for article_number in result_dict:
        article_ls = result_dict[article_number]
        for sentence in article_ls:
            del sentence['text']
            sentence['event'] = sentence.pop('events')
            event_ls = sentence['event']
            for event in event_ls:
                del event['offset']
                event['argument'] = event.pop('arguments')
                argument_ls = event['argument']
                for argument in argument_ls:
                    del argument['offset']

    # merge events to one event dictionary
    dict_result = {}
    for key, value in result_dict.items():
        dict_result[key] = {'event': []}
        for i in value:
            if str(i.keys()) == "dict_keys(['event'])":
                dict_result[key]['event'] += i['event']

    # extract date from scraped result and merge it into the dictionary
    with open(f'../Collect/Scrape/wikinews/wikinews_{topic}.json', 'r', encoding='utf-8') as f:
        json_data = f.read()
    dict1 = dict_result
    dict2 = json.loads(json_data)

    # add title under each article
    for key, value in dict1.items():
        dict1[key]['title'] = dict2[key]['heading'].strip()

    # extract the topic id in scraped file
    topic_id = list(dict2.keys())[0][0]

    # add date from scraped file to the main dictionary
    for key, value in dict1.items():
        dict1[key]['date'] = dict2[key]['date']

    # rename article tags
    for i in range(1, 81):
        try:
            dict1[f'{topic_id}-{i}']
        except KeyError:
            pass
        else:
            dict1[f'article aid={i}'] = dict1.pop(f'{topic_id}-{i}')

    # create category elements on the top level
    dict3 = {"category": dict1}

    # STEP 4: converting preprocessed dictionary to XML
    xml = dict2xml(dict3)

    # STEP 5: edit tags and attributes
    # read in the scraping results so that the links of each article can be added to the article attribute
    with open(f'../Collect/Scrape/wikinews/wikinews_{topic}.json', 'r', encoding='utf-8') as f:
        scrape_data = f.read()
        scrape_json = json.loads(scrape_data)

    # define a regular expression pattern to match the tags
    pattern = r'<article_aid_(\d+)>|</article_aid_(\d+)>'

    # define a function to replace the matched tags with the desired format
    def replace_tags(match):
        if match.group(1):
            article_id = int(match.group(1))
            aid = f"{topic_id}-{article_id}"
            return f'<article aid="{aid}" url="{scrape_json[aid]["link"]}">'
        elif match.group(2):
            return '</article>'

    # replace the tags
    new_xml_string = re.sub(pattern, replace_tags, xml)

    # define a regular expression pattern to match the tags
    pattern_category = r'<category>'

    # define a function to replace the matched tags with the desired format
    def replace_category_tags(match):
        return f'<category topic="{topic}" cid="{topic_id}"\n' \
               f'          xmlns="http://www.w3schools.com/NaturalCatastrophe"\n' \
               f'          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n' \
               f'          xsi:schemaLocation="http://www.w3schools.com/NaturalCatastrophe xml_schema.xsd">' \

    # replace the tags
    new_xml_string = re.sub(pattern_category, replace_category_tags, new_xml_string)

    # STEP 7: output the modified XML string
    with open(f'events2xml_results/{topic}.xml', 'w', encoding='utf-8') as file:
        file.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")  # XML declaration
        file.write(new_xml_string)  # XML content
