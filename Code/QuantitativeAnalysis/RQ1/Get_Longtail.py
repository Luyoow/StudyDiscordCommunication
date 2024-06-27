import json
from datetime import datetime
import emoji
import pandas as pd
import os

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_root = root + "/Data/DataJSON"                         # input：location 
res_root = root + "/Data/DataRQ/RQ1/longtail_addinfo.csv"   # output: lcation

community_dirs = os.listdir(data_root)
utterance_count = {}
com_tag = {}
res = pd.DataFrame()

for filename in community_dirs:
    filename = data_root + "/" +filename + "/" + filename + ".json"
    with open(filename,'r',encoding='utf-8') as file:
        data = json.load(file)
        for index, x in enumerate(data['messages']):
            if x['author']['isBot']:
                continue
            content = x['content']
            withoutemoji = emoji.replace_emoji(content, replace="")
            withoutemoji = withoutemoji.replace('\n', '').replace('\r', '')
            if withoutemoji == "":
                continue
            author = x['author']['nickname']
            author = emoji.demojize(author).replace(" ", "")  
            author = author.encode('utf-8')
            if author not in utterance_count.keys():
                utterance_count[author] = 1
                com_tag[author] = set()
                com_tag[author].add(filename)
            else:
                utterance_count[author] += 1
                com_tag[author].add(filename)
com_list = []
for name in utterance_count.keys():
    com_list.append(com_tag[name])

res["name"] = list(utterance_count.keys())
res["utterance_num"] = list(utterance_count.values())
res["com"] = com_list

res.to_csv(res_root)