import json
import math
# insert global variables
import time

from helpers.text_preprocessing import preprocessing

is_test = False

filename = 'data/inverted_json_file_test.json' if is_test else 'data/numbered_inverted_json_file.json'

shared_dict_map = {}

file_link_map = {}

number_of_documents = 10000


def load_link_file_map():
    _link_file = open('data/final_crawled_new.csv', 'r', encoding='utf-8')
    for line in _link_file.read().splitlines():
        row_items = line.split(',')
        file_link_map[row_items[2]] = row_items[1]


print('Load file and URL link data files.')
load_link_file_map()

# loading the inverted index file
scrapped_file = open(filename)
scrapped_data_doc = json.load(scrapped_file)

doc_len_file = open("data/doc_len.json")
doc_len_list = json.load(doc_len_file)

def query_search(query_string):
    start = time.perf_counter()
    query_array = preprocessing(query_string)
    print("query_string:: {}".format(query_array))

    # inverted index retrieval algorithm
    result = {}
        
    for item in query_array:
        max_freq = 0
        
        document_frequency = scrapped_data_doc[item]['count'] 
        
        for docs in scrapped_data_doc[item]["document_frequency"]:
            if max_freq < int(list(docs.values())[0]):
                max_freq = int(list(docs.values())[0])
        
        for docs in scrapped_data_doc[item]["document_frequency"]:
            filename = list(docs.keys())[0]
            doc_len = doc_len_list[filename]
            q_l = 1
            # calculating the term frequency
            tf = int(list(docs.values())[0]) / int(max_freq)

            #calculating the inverse document frequency
            idf = math.log(number_of_documents / document_frequency)

            similarity_measure = (tf * idf) / (doc_len * q_l)
            doc = list(docs.keys())[0]
           
            if doc in result.keys():
                result[doc] = result[doc] + similarity_measure
            else:
                result[doc] = similarity_measure

    time_delta = time.perf_counter() - start
    print('Search Duration: {}'.format(time_delta))

    # sorting the rank in decreasing order
    rank = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}

    # for mapping url and the file
    valid_ranks = []
    for item in rank.items():
        if item[1] != 0.0:
            url = file_link_map[item[0]]
            valid_ranks.append((item[0], url, item[1]))  # filename, score

    # returning only the top hundered documents
    #return valid_ranks[:100]
    return valid_ranks



