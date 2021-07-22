from flask import Flask, app, request, Response
from flask.json import jsonify
from generate_tweet import get_user_timeline
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/api/v1/generate_tweets_v1/<twittername>', methods=['GET'])
def generate_tweets(twittername):
    print(twittername)
    results = get_user_timeline(twittername)
    print(results)
    data = [{'username': twittername, 'text': result} for result in results]
    response = {
        'success': True,
        'data': data
    }
    return jsonify(response)

@app.route('/api/v1/ping', methods=['GET'])
def ping():
    response = {
        'success': True,
        'data': 'pong'
    }
    return jsonify(response)

# from http.server import BaseHTTPRequestHandler
# from datetime import datetime

# class handler(BaseHTTPRequestHandler):

#   def do_GET(self):
#     self.send_response(200)
#     self.send_header('Content-type', 'text/plain')
#     self.end_headers()
#     self.wfile.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).encode())
#     return