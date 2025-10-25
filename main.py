from flask import Flask, jsonify
from db.config import Config
from db.connection import db
from dotenv import load_dotenv
import os
from schema.schemas import Education, Job, Marital, Contact, Month, Poutcome, Prediction
from helpers.catalogs import serialize_catalog

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

port = int(os.getenv("PORT", 5000))

@app.route("/form_options", methods=["GET"])
def get_form_options():
    educations = serialize_catalog(Education.query.all())
    jobs = serialize_catalog(Job.query.all())
    marital_statuses = serialize_catalog(Marital.query.all())
    contacts = serialize_catalog(Contact.query.all())
    months = serialize_catalog(Month.query.all())
    poutcomes = serialize_catalog(Poutcome.query.all())

    return jsonify({
        "educations": educations,
        "jobs": jobs,
        "marital_statuses": marital_statuses,
        "contacts": contacts,
        "months": months,
        "poutcomes": poutcomes
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # crea tablas
    app.run(host='0.0.0.0', port=port, debug=True)
