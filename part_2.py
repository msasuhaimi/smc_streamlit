# part_2
import tweepy
from tweepy import OAuthHandler
import altair as alt
import pandas as pd
import numpy as np
from datetime import date
import networkx as nx
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt
from operator import itemgetter

# Brand Friends
nodeList = ["HyperX", "Razer", "Logitech"]
edgeList = []

dfHyperXFollowing = pd.read_csv('/content/drive/Shareddrives/SMC/HyperXFollowing.csv', index_col = 0)
dfLogitechFollowing = pd.read_csv('/content/drive/Shareddrives/SMC/LogitechFollowing.csv', index_col = 0)
dfRazerFollowing = pd.read_csv('/content/drive/Shareddrives/SMC/RazerFollowing.csv', index_col = 0)


for index, row in dfHyperXFollowing.iterrows():
  if row[0] not in nodeList:
    nodeList.append(row[0])
  edgeList.append(("HyperX", row[0]))

for index, row in dfLogitechFollowing.iterrows():
  if row[0] not in nodeList:
    nodeList.append(row[0])
  edgeList.append(("Logitech", row[0]))

for index, row in dfRazerFollowing.iterrows():
  if row[0] not in nodeList:
    nodeList.append(row[0])
  edgeList.append(("Razer", row[0]))

G = nx.Graph()
G.add_nodes_from(nodeList)
G.add_edges_from(edgeList)

pos = nx.spring_layout(G, k = 0.045)
pos = nx.spectral_layout(G)

nodelists = ['HyperX', 'Razer', 'Logitech']
labels = {'HyperX': "HyperX", 'Razer': "Razer",'Logitech': "Logitech"}
color = []
for i in nodeList:
  if i == "HyperX":
    color.append("#fe0404")
  elif i == "Razer":
    color.append("#079a03")
  elif i == "Logitech":
    color.append("#5eb1ff")



fig = plt.figure(figsize = (20,20))
nx.draw(G, pos=pos, edge_color="#dedede", node_color = "#47fff7", linewidths=0.05, node_size=20, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(G, pos=pos, node_color = color, nodelist = nodelists, node_size=500)
nx.draw_networkx_labels(G,pos,labels,font_size=16,font_color='#000000')
st.pyplot(fig)