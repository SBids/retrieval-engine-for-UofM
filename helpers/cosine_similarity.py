# # Created by: Sagar Duwal
# # Github: @sagarduwal 
# # Date: 11/14/21

# # Feature: <Feature Name>
# # <Feature Description>

# # insert import(s) here
# import concurrent.futures
# import json
# import math
# import os.path
# import pickle
# import time

# # insert global variables
# from helpers.text_preprocessing import preprocessing

# is_test = False

# filename = 'data/inverted_json_file_test.json' if is_test else 'data/numbered_inverted_json_file.json'

# shared_dict_map = {}

# file_link_map = {}


# def load_link_file_map():
#     _link_file = open('data/final_crawled_new.csv', 'r', encoding='utf-8')
#     for line in _link_file.read().splitlines():
#         row_items = line.split(',')
#         file_link_map[row_items[2]] = row_items[1]


# print('Load file and URL link data files.')
# load_link_file_map()


# # function definitions
# def count_document_list():
#     global scrapped_file
#     global scrapped_data_doc
#     scrapped_file = open(filename)
#     scrapped_data_doc = json.load(scrapped_file)
#     doc_list = []
#     for d, v in scrapped_data_doc.items():
#         for item in v['document_frequency']:
#             for e in [*item]:
#                 doc_list.append(e)
#     return set(doc_list)


# print('Loading document list data files .... ')
# filename_list = sorted(list(count_document_list()))  # get all the available file name

# scrapped_file = open(filename)
# scrapped_data_doc = json.load(scrapped_file)

# is_processing = False
# is_loading = False

# batch_filename_list = filename_list[:100]


# def process_tf_idf_for_document(vector_shared_dict, document):
#     doc_start_time = time.process_time()

#     print('Doc: {}'.format(document))

#     doc_key = document
#     doc_word_tf = []

#     for vocabulary, vocabValue in scrapped_data_doc.items():
#         tf = 0
#         for item in vocabValue['document_frequency']:
#             if str(document) in [*item]:  # if current filename match with the item in document frequency
#                 tf = item.get(document)
#         df = scrapped_data_doc[vocabulary]['count']
#         idf = math.log(len(filename_list) / (df + 1))
#         doc_word_tf.append(tf * idf)
#         vector_shared_dict[doc_key] = doc_word_tf

#     print('Time Taken for completing processing a file: {}'.format(time.process_time() - doc_start_time))
#     return vector_shared_dict


# def store_pickle(shared_dict):
#     pickle_file = 'tf_idf.pkl'

#     store_pickle = open(pickle_file, 'wb')
#     pickle.dump(shared_dict, store_pickle)
#     store_pickle.close()


# def load_pickle():
#     pickle_file = 'tf_idf.pkl'
#     stored_pickle = open(pickle_file, 'rb')

#     global shared_dict_map
#     shared_dict_map = {}
#     shared_dict_map = pickle.load(stored_pickle)


# def load_json():
#     pickle_file_json = 'gen_tf_idf.json'
#     stored_json = open(pickle_file_json, 'r')

#     global shared_dict_map
#     shared_dict_map = {}
#     shared_dict_map = json.load(stored_json)


# def generate_tf_idf(number_of_threads=5):
#     global is_processing
#     print('is_processing: {}'.format(is_processing))
#     if not is_processing:
#         print('Running processing of files.')
#         with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
#             is_processing = True
#             overall_start = time.perf_counter()

#             tf_idf_results = []
#             for doc in batch_filename_list:
#                 tf_idf_results.append(executor.submit(process_tf_idf_for_document, shared_dict_map, doc))

#             for r in tf_idf_results:
#                 shared_dict_map.update(r.result())

#             store_pickle(shared_dict_map)
#             with open('gen_tf_idf.json', 'w+', encoding='utf-8') as file:
#                 json.dump(shared_dict_map, file)

#             time_delta = time.perf_counter() - overall_start
#             print('Overall Duration: {}'.format(time_delta))
#             is_processing = False
#             return 'Over all Duration: {}'.format(time_delta)
#     else:
#         return 'Processing already in progress.'


# def get_query_vector(query_string):
#     q = preprocessing(query_string)
#     print("query_string:: {}".format(q))

#     doc_word_tf = []
#     vector_dict = {}

#     for d, v in scrapped_data_doc.items():  # for each vocab d
#         tf = 0
#         if d in q:
#             tf = q.count(d)

#         doc_word_tf.append(tf)
#         vector_dict['query'] = doc_word_tf

#     return vector_dict['query']


# def load_tfidf():
#     pickle_file = 'tf_idf.pkl'
#     pickle_file_json = 'gen_tf_idf.json'

#     if not os.path.exists(pickle_file) or not os.path.exists(pickle_file_json):
#         return 'TFIDF file does not exist'
#     if is_loading:
#         return 'TFIDF load already load in progress.'
#     else:
#         if os.path.exists(pickle_file):
#             load_pickle()
#         elif os.path.exists(pickle_file_json):
#             load_json()
#         return 'Total documents loaded: {}'.format(len(shared_dict_map.keys()))


# def clear_tfidf():
#     pickle_file = 'tf_idf.pkl'
#     if os.path.exists(pickle_file):
#         os.remove(pickle_file)
#         global shared_dict_map
#         shared_dict_map = {}
#         return 'TFIDF file cleared.'
#     else:
#         return 'TFIDF file does not exist'


# def search_tfidf(query_string):
#     start = time.perf_counter()
#     cosine_list = {}
#     query_arr = get_query_vector(query_string)

#     if len(shared_dict_map.keys()) == 0:
#         load_tfidf()
#         return 'TFIDF was not loaded yet. Loading it now. Please try again in a while.'

#     for doc in batch_filename_list:
#         vect_arr = shared_dict_map[doc]

#         numerator = 0

#         for i in range(0, len(query_arr)):  # 19 is len(vocab)
#             numerator += vect_arr[i] * query_arr[i]
#         sum_d = 0
#         for ele in vect_arr:
#             sum_d += ele * ele
#         sum_q = 0
#         for ele in query_arr:
#             sum_q += ele * ele
#         denominator = math.sqrt(sum_q * sum_d)
#         if denominator != 0:
#             cosine_list[doc] = numerator / denominator
#         # if cosine_list[doc] != 0:
#         #     print('{} : {}'.format(doc, cosine_list[doc]))

#     time_delta = time.perf_counter() - start
#     print('Search Duration: {}'.format(time_delta))
#     rank = {k: v for k, v in sorted(cosine_list.items(), key=lambda item: item[1], reverse=True)}

#     valid_ranks = []
#     for item in rank.items():
#         if item[1] != 0.0:
#             url = file_link_map[item[0]]
#             valid_ranks.append((item[0], url, item[1]))  # filename, score

#     return valid_ranks


# def get_document_length(idf,filename):
#     dl = 0.0
#     for key,value in scrapped_data_doc.items():
#         document_frequency = scrapped_data_doc[key]['count'] 
#         idf = math.log(number_of_documents / document_frequency)

#         tf_list = scrapped_data_doc[key]["document_frequency"]
#         for dict in tf_list:
#             dic_key = list(dict.keys())[0]
#             if filename == dic_key:
#                 count = math.pow(idf * int(dict[dic_key]),2)
#                 dl = dl+count
#     sq_dl = math.sqrt(dl)
#     return sq_dl
            

