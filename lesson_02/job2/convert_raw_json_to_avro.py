import json
import logging
import os
import shutil
from pathlib import Path
from fastavro import writer, parse_schema

logger = logging.getLogger(__name__)

def convert_raw_json_to_avro(stg_dir: str, raw_dir: str):
    # clear raw dir from all files
    shutil.rmtree(stg_dir, ignore_errors=True)

    # create directory for raw dir if not exists
    os.makedirs(stg_dir, exist_ok=True)

    with open('schema.json', 'r') as f:
        parsed_schema = parse_schema(json.load(f))

    total_records = 0

    for file_path in Path(raw_dir).iterdir():
        with file_path.open('r') as json_file:
            json_data = json.load(json_file)

        with open(f"{stg_dir}/{file_path.stem}.avro", 'wb') as out:
            writer(out, parsed_schema, json_data)

        total_records += len(json_data)

    logger.info(f"Total records converted: {total_records}")

