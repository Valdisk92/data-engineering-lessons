import logging

from flask import Flask, request
from flask import typing as flask_typing

from lesson_02.job2.convert_raw_json_to_avro import convert_raw_json_to_avro

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    input_data: dict = request.json
    stg_dir = input_data.get('stg_dir')
    raw_dir = input_data.get('raw_dir')

    if not stg_dir:
        return {
            "message": "stg_dir parameter missed",
        }, 400

    if not raw_dir:
        return {
            "message": "raw_dir parameter missed",
        }, 400

    convert_raw_json_to_avro(stg_dir, raw_dir)

    return {
        "message": "Data converted successfully from JSON to Avro.",
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)
