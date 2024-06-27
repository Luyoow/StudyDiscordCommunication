import os
import emoji
import json

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")) # get ccurrent dir
data_root = root + "/Data/DataJSON"  # input : location
TXT_root = root + "/Data/DataTXT"    # output : location

count = 0
au = set()
size=0
community_dirs = os.listdir(data_root)
for community_dir in community_dirs:
    print(community_dir)
    json_name = os.listdir(data_root + "/" + community_dir)[0]         # get JSON file name
    #print(data_root + "//" + community_dir + "//" + json_dir)
    json_dir = data_root + "/" + community_dir + "/" + json_name 
    with open (json_dir, "r", encoding="utf-8") as file:
        community_json = json.load(file)
    #new_dir = json_dir.replace("json", "txt").replace("DataJSON", "DataTXT") 
    os.makedirs(TXT_root + "/" + community_dir)                       # make new directory
    new_dir = TXT_root + "/" + community_dir + "/" + json_name.replace("json", "txt")
    with open(new_dir, 'w', encoding="utf-8") as new_file:
        cnt = {}    
        for x in community_json['messages']:
            if x['author']['isBot']:
                continue
            day = x['timestamp'].split("T")[0]       # day
            time = x['timestamp'].split("T")[1].split(".")[0].split("+")[0]
            author = x['author']['nickname']
            author = emoji.demojize(author).replace(" ", "")                # Remove the emoji (demojize -> replaced with a special character) and spaces from the name
            content = x['content']
            withoutemoji = emoji.replace_emoji(content, replace="")
            withoutemoji = withoutemoji.replace('\n','').replace('\r','')   # previous mistake: make "r" disappear here
            if withoutemoji != "":
                swrite = "["+day+" "+time+"]"+" "+"<"+author+">"+" "+ withoutemoji
                new_file.write(swrite+'\n')
                count = count+1
                if author not in au:
                    au.add(author)
                    size = size+1
    #print("utterances:", count, "Participants:", size)