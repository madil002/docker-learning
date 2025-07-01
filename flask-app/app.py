from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def welcome():
    return "Welcome"

@app.route('/count')
def count():
    count = r.incr('visit_count')
    
    return f'You have visited this site {count} times.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
