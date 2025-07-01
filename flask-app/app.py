import os
from flask import Flask
import redis

app = Flask(__name__)
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

@app.route('/')
def welcome():
    return "Welcome"

@app.route('/count')
def count():
    count = r.incr('visit_count')
    
    return f'You have visited this site {count} times.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
