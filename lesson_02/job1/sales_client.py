import logging
import requests
import os

logger = logging.getLogger(__name__)

class SalesClient:
    def __init__(self, api_url: str, auth_token: str):
        self.auth_token = auth_token
        self.url = api_url

    def get_sales_transactions(self, date: str, page: int = 1) -> object:
        logger.info(f"Performing request to {self.url} for {page} for date {date}")

        if not self.auth_token:
            raise NoAuthTokenError()

        response = requests.get(
            url=self.url,
            params={'date': date, 'page': page},
            headers={'Authorization': self.auth_token},
        )

        if response.status_code != 200:
            return None

        return response.json()


class NoAuthTokenError(Exception):
    def __init__(self):
        self.message = "API_AUTH_TOKEN is not set. Set it as env var"
        super().__init__(self.message)