import os
import shutil
from lesson_02.job1.sales_client import SalesClient

def save_sales_to_local_dir(date: str, raw_dir: str) -> None:
    # clear raw dir from all files
    shutil.rmtree(raw_dir, ignore_errors=True)

    # create directory for raw dir if not exists
    os.makedirs(raw_dir, exist_ok=True)

    sales_client = SalesClient()

    page = 1
    while True:
        data = sales_client.get_sales_transactions(date, page)
        if data is None:
            break
        write_to_file(data, date, page, raw_dir)
        page += 1


def write_to_file(data, date, page, raw_dir):
    with open(f"{raw_dir}/sales_{date}_{page}.json", "w") as f:
        f.write(data)
