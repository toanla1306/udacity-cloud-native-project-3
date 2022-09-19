from flask import Flask, render_template, request, jsonify

import os
import pymongo
import logging
from flask_pymongo import PyMongo

from prometheus_flask_exporter import PrometheusMetrics

from jaeger_client import Config
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Configure Jaeger tracer
def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
        validate=True
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

app = Flask(__name__)
tracer = init_tracer('backend')
FlaskInstrumentor().instrument_app(app)

metrics = PrometheusMetrics(app)
metrics.info('backend', 'Backend Application info', version='1.0.3')

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

record_requests_by_status = metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})

common_counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)

historgram_status_path = metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path', labels={'status': lambda r: r.status_code, 'path': lambda: request.path})

@app.route("/")
@record_requests_by_status
@common_counter
def homepage():
    with tracer.start_active_span('home-page'):
        return "Hello World"


@app.route("/api")
@record_requests_by_status
@common_counter
@historgram_status_path
def my_api():
    with tracer.start_span('my-api'):
        answer = "something"
        return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
@record_requests_by_status
@common_counter
@historgram_status_path
def add_star():
    with tracer.start_span('add star'):
        star = mongo.db.stars
        name = request.json["name"]
        distance = request.json["distance"]
        star_id = star.insert({"name": name, "distance": distance})
        new_star = star.find_one({"_id": star_id})
        output = {"name": new_star["name"], "distance": new_star["distance"]}
        return jsonify({"result": output})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
