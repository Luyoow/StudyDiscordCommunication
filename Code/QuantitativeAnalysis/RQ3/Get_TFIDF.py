from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
import datetime 
import os
import pandas as pd


#A list of all sentences within the first thirty days of the initial sentence of the dialogue needs to be extracted
#218243[2021-12-16 16:14:45] <AlexBrito> I mean this was for an interview problem\

def Get_Last_30(utter, community_name):
    raw_file = open(community_name, "r", encoding= "utf-8")
    lines = raw_file.readlines()
    index = int(utter[ : utter.find("[")])
    start_time = datetime.datetime.strptime(utter[utter.find("[") + 1 : utter.find("] ")], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(days = 30)
    user_message = []
    for i in range(index - 2, -1, -1):  #Count forward from the current sentence
        per_line = lines[i]
        #print(per_line)
        daytime = per_line[per_line.find("[") + 1 : per_line.find("] ")]
        #print(daytime)
        nowtime = datetime.datetime.strptime(daytime, "%Y-%m-%d %H:%M:%S")
        content = per_line[per_line.find("> ") + 2:]
        #name = per_line[per_line.find(' <') + 2 : per_line.find('> ')]
        #if (name not in user_message.keys()):
            #user_message[name] = 0
        if (nowtime > start_time):
            user_message.append(content)
            
        else:
            break
            #print(name)
    return user_message

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_dir = root + "/Data/DataAscii/Manual/"              # input：location 
res_dir = root + "/Data/DataRQ/RQ3/Similarity/"                 # output: lcation

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

com_dirs = os.listdir(data_dir)

for com in com_dirs:
    com_dir = data_dir + com
    community_name = com.split(".")[0]
    community_dir = root + "/Data/DataAscii/" + community_name + ".txt"
    # if (com == "android.txt"):
    #     continue
    print(com)
    
    data_df = pd.DataFrame({"DialogNum":[], "similarity":[]})
    with open(com_dir, 'r', encoding= "GB2312") as f:
        first_utterance_flag = 1    # Mark whether the current sentence is a dialogue starter
        lines = f.readlines()
        dialog_count = 1
        res_index = []
        res_similarity = []
        for index, line in enumerate(lines):
            if (first_utterance_flag == 1):
                first_utterance_flag = 0
                dialog_count += 1
                #print(line)
                utter = line
                data = Get_Last_30(utter, community_dir)

                texts = [lcut(s) for s in data]
                dictionary = Dictionary(texts)
                corpus = [dictionary.doc2bow(text) for text in texts]
                tfidf = TfidfModel(corpus)      # Training a model with a corpus
                tf_texts = tfidf[corpus]        # Using the corpus as the searched data
                sparse_matrix = SparseMatrixSimilarity(tf_texts, len(dictionary)) 

                keyword = utter
                kw_vector = dictionary.doc2bow(lcut(keyword))

                tf_kw = tfidf[kw_vector]
                
                similarities = sparse_matrix.get_similarities(tf_kw)
                max_similar = -1
                for e, s in enumerate(similarities):
                    if (s > max_similar):
                        max_similar = s
                print('the biggest similarity:%.2f' % max_similar)
                res_similarity.append(max_similar)

            if (line == "-------" + str(dialog_count - 1) + '\n'):
                first_utterance_flag = 1          #Explain that the next sentence begins with the first sentence of the dialog
                res_index.append(dialog_count - 1)
    #res_index.append
    #data_df["DialogNum"] = res_index
    data_df["similarity"] = res_similarity
    data_df.to_csv(res_dir + com + "_sim.csv")
    #break            
