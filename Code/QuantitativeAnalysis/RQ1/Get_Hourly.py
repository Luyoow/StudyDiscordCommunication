import json
from datetime import datetime
import emoji
import pandas as pd
import os


def gethour(timestamp):
    time = timestamp.split("T")[1].split(".")[0]
    hourstring = time.split(":")[0]
    hour = int(hourstring)%24  # Get hour
    return hour


root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_root = root + "/Data/DataJSON"                     # input：location 
res_root = root + "/Data/DataRQ/RQ1/hourly.csv"         # output: lcation

community_dirs = os.listdir(data_root)
res_weekly = pd.DataFrame()

for filename in community_dirs:
    distribution = [0 for x in range(24)]
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
            timestamp = x["timestamp"]
            i = gethour(timestamp)
            distribution[i] = distribution[i]+1
    res_weekly[filename] = distribution
    
res_weekly.to_csv(res_root)