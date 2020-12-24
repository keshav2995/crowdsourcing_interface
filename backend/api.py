from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
app.config["CORS_ALWAYS_SEND"] = True
app.config["CORS_SEND_WILDCARD"] = True
app.config['CORS_ORIGINS'] = ['null', '*']
app.config['CORS_HEADERS'] = ['Content-Type']

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///warrants.sqlite"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Warrant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warrant = db.Column(db.String, unique=True, nullable=False)


def calculate(warrant):
    """return quality score of the warrant"""

    return {"score": 1, "warrant": warrant}


@app.route("/", methods=["GET", "POST", "PUT"])
def analyze():
    if request.method == "GET":
        warrant = request.args.get(
            "warrant", default="", type=str
        )  # get the warrant to be analyzed
        score = calculate(warrant)  # analyze the warrant and return the score
        return jsonify(score)
    elif request.method == "PUT":
        payload = request.json
        warrant = Warrant(payload.get("warrant"))  # create the warrant db object
        db.session.add(warrant)  # stage the warrant for saving
        db.session.commit()  # save the warrant
        return jsonify(warrant.to_dict())  # return the saved warrant
    else:
        return jsonify({"details": "welcome to the api"})

@app.route("/save", methods=["GET", "POST", "PUT"])
def save():
        warrant = request.args.get(
            "warrant", default="", type=str
        )  # get the warrant to be analyzed
        warrant = Warrant(warrant = warrant)  # create the warrant db object
        db.session.add(warrant)  # stage the warrant for saving
        db.session.commit()  # save the warrant
        return jsonify({'id': warrant.id, 'warrant': warrant.warrant})  # return the saved warrant

if __name__ == "__main__":
    app.run(debug=True)
