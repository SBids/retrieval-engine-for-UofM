from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from helpers.search_algo import *


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search', methods=['POST'])
def tfidf_search():
    req_body = request.get_json()
    query_string = req_body['query']
    # calling the function in search_algo.py
    response = query_search(query_string)
    return jsonify({'message': response})


if __name__ == "__main__":
    app.run()
