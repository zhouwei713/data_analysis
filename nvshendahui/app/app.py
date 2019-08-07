# coding = utf-8
"""
@author: zhou
@time:2019/8/6 10:10
@File: app.py
"""

from flask import Flask, render_template, g, request, jsonify
import os
import pandas as pd
import sqlite3
from tools import deal_data, deal_html
import random
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hardtohard'
    SQLALCHEMY_DATABASE_URI = os.path.join(basedir, 'nvshen.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    NO_PIC = ('https://img1.qunliao.info/fastdfs3/M00/73/C6/ChOxM1vG51KAc8lHAAWteFNO4iE816.jpg',
              'https://img1.qunliao.info/fastdfs4/M00/C9/4C/ChMf8Fyy5siATDnJAAHnwjyiUko688.jpg',
              'https://img1.qunliao.info/fastdfs4/M00/CA/BA/ChNLkl0XaqyABPl7AAGI0ZLPD50274.jpg',
              'https://img1.qunliao.info/fastdfs3/M00/73/C6/ChOxM1vG5_mAfi_YAAWteFNO4iE389.jpg',
              'https://img1.qunliao.info/fastdfs3/M00/80/32/ChOxM1ve5kuARaGwAAUDrq_brKs349.jpg',
              'https://img1.qunliao.info/fastdfs3/M00/99/26/ChOxM1wRzPuAJ9VmAAVzreDFLbM847.jpg',
              'https://img1.qunliao.info/fastdfs3/M00/AA/81/ChOxM1wzBu6AYMQrAAHo69qprd4770.jpg', )

    @staticmethod
    def init_app(app):
        pass


app.config.from_object(Config)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# @app.route('/init')
def init():
    init_db()
    return "OK"


# @app.route('/insert')
def insert():
    db = get_db()
    nvshen_list = deal_data()
    print(nvshen_list)
    for nvshen in nvshen_list:
        db.execute('insert into nvshen (name, nvshen_id) values (?, ?)', [nvshen[0], nvshen[1]])
    db.commit()
    return "OK"


# @app.route('/insert_pic')
def insert_pic():
    db = get_db()
    cur = db.execute('select name, nvshen_id from nvshen order by id desc')
    nvshen = [dict(name=row[0], nvshen_id=row[1]) for row in cur.fetchall()]
    nopic = app.config['NO_PIC']
    for n in nvshen:
        url_list = deal_html(str(n['nvshen_id']) + ".html", nopic)
        # print(url_list)
        for url in url_list:
            db.execute('insert into picture (nvshen_id, pic_url) values (?, ?)', [n['nvshen_id'], url])
    db.commit()
    return "OK"


@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    cur = db.execute('select name, nvshen_id from nvshen order by id desc')
    nvshen = [dict(name=row[0], nvshen_id=row[1]) for row in cur.fetchall()]
    data = []
    socre = 1
    for n in nvshen:
        tmp_data = []
        pic = db.execute('select pic_url from picture where nvshen_id = (?)', [n['nvshen_id']])
        pic_list = [row[0] for row in pic.fetchall()]
        pic_url = random.choice(pic_list)
        tmp_data.append(n['name'])
        tmp_data.append(pic_url)
        tmp_data.append(n['nvshen_id'])
        data.append(tmp_data)
    return render_template('index.html', data=data, score=socre)


@app.route('/nvshen/<id>/', methods=['GET', 'POST'])
def nvshen(id):
    db = get_db()
    user_ip = request.remote_addr
    user_score = db.execute('select score from score where nvshen_id = (?) and userip = (?)', [id, user_ip]).fetchone()
    pic = db.execute('select pic_url from picture where nvshen_id = (?)', [id])
    pic_list = [row[0] for row in pic.fetchall()]
    pic_url = random.choice(pic_list)
    if user_score is None:
        score = 0
    else:
        score = user_score[0]
    return render_template('nvshen.html', nvshenid=id, main_url=pic_url, pic_list=pic_list, user_score=score)


@app.route('/api/score/', methods=['POST'])
def set_score():
    db = get_db()
    data = request.get_data().decode('utf-8')
    data_dict = json.loads(data)
    print(data_dict)
    # nvshenid = request.form.get("nvshenid", "")
    # score = request.form.get("score", "")
    setScore_ip = request.remote_addr
    nvshenid = data_dict['nvshenid']
    score = data_dict['score']
    checkpoint = db.execute('select id from score where nvshen_id = (?) and userip = (?)', [nvshenid, setScore_ip]).fetchone()
    if checkpoint is None:
        db.execute('insert into score (nvshen_id, score, userip) values (?, ?, ?)', [nvshenid, score, setScore_ip])
    else:
        db.execute('update score set score = (?) where id = (?)', [score, checkpoint[0]])
    db.commit()
    return jsonify({"msg": "OK", "code": 200})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
