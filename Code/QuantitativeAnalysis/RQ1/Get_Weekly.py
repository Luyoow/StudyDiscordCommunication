import json
from datetime import datetime
import emoji
import pandas as pd
import os

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_root = root + "/Data/DataJSON"                     # input：location 
res_root = root + "/Data/DataRQ/RQ1/weekly.csv"         # output: lcation

community_dirs = os.listdir(data_root)
res_weekly = pd.DataFrame()

for filename in community_dirs:
    count = [0 for i in range(7)]
    filename = data_root + "/" +filename + "/" + filename + ".json"
    with open(filename,'r',encoding='utf-8') as file:
        data = json.load(file)
        for x in data['messages']:
            if x['author']['isBot']:
                continue
            content = x['content']
            withoutemoji = emoji.replace_emoji(content, replace="")
            withoutemoji = withoutemoji.replace('\n', '').replace('r', '')
            if withoutemoji == "":
                continue
            daytime = x['timestamp']
            day = daytime.split("T")[0]
            index = datetime.strptime(day,"%Y-%m-%d").weekday()
            count[index] = count[index]+1
    res_weekly[filename] = count
res_weekly.to_csv(res_root)