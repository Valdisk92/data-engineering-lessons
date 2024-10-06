import logging
from flask import Flask, request
from flask import typing as flask_typing

from lesson_02.job1.save_sales_service import save_sales_to_local_dir

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    input_data: dict = request.json
    date = input_data.get('date')
    raw_dir = input_data.get('raw_dir')

    if not date:
        return {
            "message": "date parameter missed",
        }, 400

    save_sales_to_local_dir(date=date, raw_dir=raw_dir)

    return {
        "message": "Data retrieved successfully from API",
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8081)
