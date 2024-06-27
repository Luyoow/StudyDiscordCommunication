import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_dir = root + "/Data/DataRQ/RQ3/Similarity/ALL_merge.csv"                     # input：location 


data = pd.read_csv(data_dir)
plt.figure(figsize=(15,3))

my_order = data.groupby(by=["Topic"])["similarity"].median() #.index
medians = data.groupby(by=["Topic"])["similarity"].median().values

my_order = ["API Usage", "Review", "Do not work", "Reliability Issue","Performance Issue", "Test/Build Failure", "Error", "API Change", "Background Info","New Features", "Design", "Learning", "Others"]
for (i, TopicName) in enumerate(my_order):
    if (i >= 2):
        data["Topic"] = data["Topic"].replace(i + 2, TopicName)
    else:
        data["Topic"] = data["Topic"].replace(i + 1, TopicName)

ax = sns.violinplot(x="Topic", y="similarity", data=data, density_norm='width',
                cut=0, inner=None,
                palette=sns.color_palette("YlGnBu"), linewidth=0.5) # YlGnBu  #hls
plt.setp(ax.collections, alpha=.7)
ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
plt.subplots_adjust(bottom=0.2)
ax.set_xlabel('Topic')
ax.set_ylabel('Singularity')

g = sns.boxplot(data=data, x='Topic', y='similarity', showfliers=False, linewidth=0.7, width = 0.2)

median_labels = [str(np.round(s, 2)) for s in medians]

pos = range(len(medians))
for tick,label in zip(pos,g.get_xticklabels()):
    g.text(pos[tick], medians[tick], median_labels[tick], 
            horizontalalignment='center', size='x-small', color='Black')


for i in range(len(g.artists)):
    box = g.artists[i]
    box.set_edgecolor('black')
    box.set_facecolor('white')
    for j in range(5):
        k = i*5 + j
        line = g.lines[k]
        line.set_color('black')
        
plt.show()