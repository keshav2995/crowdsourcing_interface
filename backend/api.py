from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import exc
from sentence_transformers import SentenceTransformer
import scipy
embedder = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')

app = Flask(__name__)
app.config["CORS_ALWAYS_SEND"] = True
app.config["CORS_SEND_WILDCARD"] = True
app.config["CORS_ORIGINS"] = ["null", "*"]
app.config["CORS_HEADERS"] = ["Content-Type"]

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///warrants.sqlite"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Warrant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warrant = db.Column(db.String, unique=True, nullable=False)
    initial_warrant = db.Column(db.Text, nullable=False)


def calculate(warrant):
    """return quality score of the warrant"""
    warrant_kb = [warrant.warrant for warrant in Warrant.query.all()]
    user_warrant = warrant
    warrant_kb_emb = embedder.encode([warrant_kb])
    user_warrant_emb = embedder.encode([user_warrant])

    dist = scipy.spatial.distance.cdist([user_warrant_emb], warrant_kb_emb, "cosine")[0]
    sim_score = 1 - dist

    return {"score": sim_score, "warrant": warrant}


@app.route("/", methods=["GET", "POST", "PUT"])
def analyze():
    if request.method == "GET":
        warrant = request.args.get(
            "warrant", default="", type=str
        )  # get the warrant to be analyzed
        score = calculate(warrant)  # analyze the warrant and return the score
        return jsonify(score)
    elif request.method == "PUT":
        warrant = request.json
        init_warrants = " [SEP] ".join(warrant['initial_warrants'])
        warrant = Warrant(warrant=warrant['warrant'], initial_warrant = init_warrants)  # create the warrant db object
        db.session.add(warrant)  # stage the warrant for saving
        try:
            db.session.commit()  # save the warrant
        except exc.IntegrityError as e:
            response = jsonify(
                {"error": "warrant has to be unique"}
            )
            response.status_code = 403
            return response
        return jsonify(
            {"id": warrant.id, "warrant": warrant.warrant, "initial_warrant": warrant.initial_warrant}
        )  # return the saved warrant
    else:
        return jsonify({"details": "welcome to the api"})


if __name__ == "__main__":
    app.run(debug=True)
