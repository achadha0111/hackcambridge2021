from flask import Flask, request, Response, jsonify
from firebase import firebase
import os
import random
import json
import pyodbc

app = Flask(__name__)

server = os.getenv('SERVER')
database = 'votingDB'
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
driver = '{ODBC Driver 17 for SQL Server}'


@app.route('/feed', methods=["GET"])
def get_feed_items():
    feed_items = request_feed_items()
    print (feed_items)
    result = jsonify(json.loads(feed_items))
    result.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    return result, 200


# @app.route('/postevent', methods=["POST"])
# def post_user_interactions(interactions):
#     pass


"Returns some random cards from the database"


def request_feed_items():
    # noinspection SqlResolve
    query = "SELECT top 10 percent CARD.CARDTYPE, " \
            "opinion.sourcelink as opinion_source, headline, leaning, " \
            "ISFAKE, STARTTIME, ENDTIME, video.sourcelink " \
            "from [dbo].[CARD] as card FULL JOIN [dbo].[POLIOPINION] " \
            "as opinion on card.CARDID = opinion.CARDID " \
            "FULL JOIN [dbo].[VIDEO] as video ON card.CARDID = video.CARDID ORDER BY newid()" \
            "FOR JSON PATH"


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
