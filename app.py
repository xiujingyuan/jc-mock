# -*-  encoding:utf-8  -*-
from flask import Flask
from sqlalchemy import true

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
