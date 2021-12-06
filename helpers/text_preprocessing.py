import re
from string import punctuation

from helpers import porterstemmer


def preprocessing(content):
    # lowercase
    # punctuation, html tags, urls remove
    # digits remove
    # remove stopwords
    # stemming
    content = remove_html_xml_tags(content)
    content = remove_urls(content)
    content = remove_punctuation(content)
    content = remove_digits(content)
    content = remove_stopwords(content)
    content = removing_morphological_variation(content)
    return content


# removing html tags
def remove_html_xml_tags(text):
    return re.sub('<[^<]+?>', '', text)


# removing the digits
def remove_digits(text):
    return ''.join(c for c in text if not c.isnumeric())


# removing the punctuation
def remove_punctuation(text):
    return ''.join(c for c in text if c not in punctuation)


# removing the urls
def remove_urls(text):
    return re.sub(r'http\S+', '', text)


# removing stopwords
def remove_stopwords(content):
    stopword_list = []
    stopword_file_path = './data/english.stopwords.txt'
    with open(stopword_file_path, 'r', encoding='utf-8') as stop_word_list:
        stopword_list = set(stop_word_list.read().split())
    # converting all words to lowercase
    text = content.lower()
    text_words = text.split()
    stopwords_cleaned = [word for word in text_words if word not in stopword_list]
    return sorted(stopwords_cleaned)


# removing morphological variation
def removing_morphological_variation(content):
    PorterStemmer = porterstemmer.PorterStemmer()
    stemmed_word_list = []
    for word in content:
        stemmed_word = PorterStemmer.stem(word, 0, len(word) - 1)
        stemmed_word_list.append(stemmed_word)
    return sorted(stemmed_word_list)
