from flask import Flask, jsonify
from flask_cors import CORS 
from api.oanda_api import OandaApi
import http
from scraping.fx_calendar import fx_calendar

app = Flask(__name__)
CORS(app)

def get_response(data):
    if data is None:
        return jsonify(dict(message='error getting data')), http.HTTPStatus.NOT_FOUND
    else:
        return jsonify(data)
    

@app.route("/api/test")
def test():
    return jsonify(dict(message='hello'))
'''
@app.route("/api/headlines")
def headlines():
    return get_response(bloomberg_com())

@app.route("/api/account")
def account():
    return get_response(OandaApi().get_account_summary())

@app.route("/api/technicals/<pair>/<tf>")
def technicals(pair, tf)
    return get_response(get_pair(pair, tf))

@app.route("/api/prices/<pair>/<granularity>/<count>")
def prices(pair, granularity, count):
    return get_response(OandaApi().web_api_candles(pair, granularity, count))
'''
if __name__ == "__main__":
    app.run(debug=True)

