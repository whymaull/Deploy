from flask import Flask
import pymysql
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello from Railway + Flask + MySQL!'

if __name__ == '__main__':
    app.run(debug=True)
