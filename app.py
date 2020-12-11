from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)

app.confir["SQLALCHEMY_DATABASE_URI"] = "postgres://gzrkczxqihabxm:89fcdcec42ee20182d9ba09e49d32bb6f4361f8e02e9bf92c23a6b5bb811531d@ec2-54-208-233-243.compute-1.amazonaws.com:5432/d4p6ks1t0hops9"

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)
Heroku(app)





if __name__ == "__main__":
    app.run(debug=True)