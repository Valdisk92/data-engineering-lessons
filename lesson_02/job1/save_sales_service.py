import os
import shutil
import logging
import requests

logger = logging.getLogger(__name__)
AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN")
URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'

if not AUTH_TOKEN:
    print("AUTH_TOKEN environment variable must be set")


def save_sales_to_local_dir(date: str, raw_dir: str) -> None:
    # create directory for raw dir if not exists
    os.makedirs(raw_dir, exist_ok=True)

    # clear raw dir from all files
    clear_raw_dir(raw_dir)

    page = 1

    while True:
        logger.info(f"Performing request to {URL} for {page} for date {date}")
        response = requests.get(
            url=URL,
            params={'date': date, 'page': page},
            headers={'Authorization': AUTH_TOKEN},
        )

        if response.status_code == 404:
            break

        with open(f"{raw_dir}/sales_{date}_{page}.json", "w") as f:
            f.write(response.text)

        page += 1


def clear_raw_dir(raw_dir):
    for filename in os.listdir(raw_dir):
        file_path = os.path.join(raw_dir, filename)

        # Check if it's a file or directory and remove accordingly
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
