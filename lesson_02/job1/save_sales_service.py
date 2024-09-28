import json
import logging
import os
import shutil
from lesson_02.job1.sales_client import SalesClient

logger = logging.getLogger(__name__)

API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'
AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN")

def save_sales_to_local_dir(date: str, raw_dir: str, sales_client=None) -> None:
    # clear raw dir from all files
    shutil.rmtree(raw_dir, ignore_errors=True)

    # create directory for raw dir if not exists
    os.makedirs(raw_dir, exist_ok=True)

    if sales_client is None:
        sales_client = SalesClient(api_url=API_URL, auth_token=AUTH_TOKEN)

    page = 1
    total_records = 0
    while True:
        data = sales_client.get_sales_transactions(date, page)
        if data is None:
            break
        total_records += len(data)
        write_to_file(data, date, page, raw_dir)
        page += 1

    logger.info(f"Total raw records saved: {total_records}")


def write_to_file(data, date, page, raw_dir):
    with open(f"{raw_dir}/sales_{date}_{page}.json", "w") as f:
        f.write(json.dumps(data))
