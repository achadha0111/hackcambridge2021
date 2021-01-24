from flask import Flask, request, Response, jsonify
from firebase import firebase
import os
import random
import json
import pyodbc
from flask_cors import CORS, cross_origin

app = Flask(__name__)

server = os.getenv('SERVER')
database = 'votingDB'
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
driver = '{ODBC Driver 17 for SQL Server}'


@app.route('/feed', methods=["GET"])
def get_feed_items():
    feed_items = request_feed_items()
    result = jsonify(json.loads(feed_items))
    result.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    return result, 200


@app.route('/postevent', methods=['POST', 'OPTIONS'])
@cross_origin()
def post_user_interactions():
    dictionary = request.get_json()
    print(dictionary)
    fakescore = 0
    leaning = 0
    poli_num = 0
    uid = 100
    # zipped = zip(cids, types, interactions)
    query = ("select COUNT(*) from interacted where userid = {}").format(uid)
    prev_num = run_query(query)
    query = ("select fakeability from users where userid = {}").format(uid)
    prev_poli = run_query(query)
    query = ("select leaning from users where userid = {}").format(uid)
    prev_lean = run_query(query)

    no_count_query = "SET NOCOUNT ON;"
    run_query(no_count_query)

    for elem in dictionary["userInteractionEvents"]:
        if ((elem["type"] == 'V') or (elem["type"] == 'H')):
            isfake = elem["isfake"]
            if ((isfake == True and elem["rating"] == 1) or (isfake == False and elem["rating"] == 0)):
                fakescore += 1

        if elem["type"] == 'P':
            lean = elem["leaning"]
            diff = lean - int(elem["rating"])
            leaning += diff
            poli_num += 1
            # print (leaning)

        query = "insert into interacted(userid, cardid, response) values ({}, {}, {});".format(uid, elem["card_id"],
                                                                                              elem["rating"])

        print (query)
        run_query(query)

    if prev_num / 2 + len(dictionary) - poli_num != 0:
        fakescore = (prev_poli * (prev_num / 2) + fakescore) / ((prev_num / 2) + len(dictionary) - poli_num)
    if prev_num / 2 + poli_num != 0:
        leaning = (prev_lean * (prev_num / 2) + leaning) / ((prev_num / 2) + poli_num)

    query = ("update users set fakeability = {}, leaning = {} where userid = {};").format(fakescore, leaning, uid)
    run_query(query)


"Returns some random cards from the database"


def request_feed_items():
    # noinspection SqlResolve
    query = "SELECT top 5 percent card.CARDID, CARD.CARDTYPE, " \
            "opinion.sourcelink as opinion_source, opinion.headline as opheadline, leaning, " \
            "video.ISFAKE as vfake, STARTTIME, ENDTIME, video.sourcelink, headline.ISFAKE as hfake, " \
            "headline.newsoutlet, headline.headline as fheadline " \
            "from [dbo].[CARD] as card FULL JOIN [dbo].[POLIOPINION] " \
            "as opinion on card.CARDID = opinion.CARDID " \
            "FULL JOIN [dbo].[VIDEO] " \
            "as video ON card.CARDID = video.CARDID" \
            " FULL JOIN [dbo].[HEADLINE] as headline" \
            " ON card.CARDID = headline.CARDID ORDER BY newid()" \
            "FOR JSON PATH"
    print(query)
    query_result = run_query(query)

    return query_result


def run_query(query):
    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return list(cursor)[0][0]


if __name__ == "__main__":
    app.run()
