from anytree import Node, RenderTree, search
from anytree.exporter import DotExporter
from graphviz import Source
import re

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sid_obj = SentimentIntensityAnalyzer()
from textblob import TextBlob
from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer('all-MiniLM-L6-v2')
from sklearn.cluster import KMeans

def make_map(list_child_parent):
    has_parent = set()
    all_items = {}
    
    for child, parent in list_child_parent:
        if parent not in all_items:
            all_items[parent] = {}
            
        if child not in all_items:
            all_items[child] = {}
        
        all_items[parent][child] = all_items[child]
        has_parent.add(child)

    result = {}
    
    for key, value in all_items.items():
        if key not in has_parent:
            result[key] = value
    
    return result

def createTree(tree_dict, root):
    for key, item in tree_dict.items():
        child = Node(key, parent=root)

        if tree_dict[key] != '':
            createTree(tree_dict[key], child)
        else:
            return
        
def traceConversation(dataframe, tree, node):
    # parent = search.find_by_attr(tree, node).children
    
    print("All child nodes:")
    children_nodes_list = getAllChildNodes(tree, node, [])
    
    print()
    new = search.find_by_attr(tree, node)
    printGraph(new)
    
    return dataframe[(dataframe['reply_to'].isin(children_nodes_list)) | (dataframe['id'].isin(children_nodes_list + [node])) | (dataframe['reply_to_id'].isin(children_nodes_list)) | (dataframe['new_id'].isin(children_nodes_list + [node]))]

def getAllChildNodes(tree, node, children_nodes_list):
    children_nodes = search.find_by_attr(tree, node).children
    
    for i in children_nodes:
        print(i.name)
        children_nodes_list.append(i.name)
        
        if i.children != None:
            getAllChildNodes(tree, i.name, children_nodes_list)
            
        else:
            return
            
    return children_nodes_list

def printGraph(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
        
def cleanComments(comments_array):
    sentences = []

    for i in comments_array:
        sequence = i.replace('\n', ' ') # Remove new line characters
        sequence = sequence.replace('\.', '')
        sequence = sequence.replace('.', '')
        sequence = sequence.replace(",", " ")
        sequence = sequence.replace("'", " ")
        sequence = sequence.replace('\\', '')
        sequence = sequence.replace('\'s', '')
        sequence = sequence.replace('&gt;', '') # Remove ampersand
        sequence = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", sequence) # Remove the user name
        sentences.append(sequence)

    return sentences

def getSentimentalResults(vaderObject, sentence):
    textBlobResult = TextBlob(sentence)
    vaderResult = vaderObject.polarity_scores(sentence)
    compoundScore = vaderResult.pop('compound')

    return textBlobResult.sentiment.polarity, textBlobResult.sentiment.subjectivity, vaderResult, compoundScore

def getClusters(allSentences, embedder, num_clusters = 2):
    corpus_embeddings = embedder.encode(allSentences)

    # Perform kmean clustering
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append([allSentences[sentence_id], sentence_id])

    return cluster_assignment