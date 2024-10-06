import os
import shutil
from pathlib import Path

import pytest
from unittest.mock import patch, call

from lesson_02.job1.save_sales_service import save_sales_to_local_dir



@patch("lesson_02.job1.sales_client.SalesClient")
def test_save_sales_to_local_dir_success(MockSalesClient, monkeypatch):
    mock_sales_client = MockSalesClient()
    mock_sales_client.get_sales_transactions.side_effect = [
        [{"id": 1, "amount": 100}],
        None
    ]

    # given
    raw_dir = "/tmp/raw_sales"
    date = "2023-01-01"

    save_sales_to_local_dir(date=date, raw_dir=raw_dir, sales_client=mock_sales_client)

    assert mock_sales_client.get_sales_transactions.call_count == 2
    mock_sales_client.get_sales_transactions.assert_has_calls([
        call(date, 1),
        call(date, 2)
    ])

    with open(f"/tmp/raw_sales/sales_{date}_1.json", "r") as f:
        assert f.read() == '[{"id": 1, "amount": 100}]'

    shutil.rmtree(raw_dir, ignore_errors=True)


@patch("lesson_02.job1.sales_client.SalesClient")
@patch("shutil.rmtree")
@patch("os.makedirs")
@patch("lesson_02.job1.save_sales_service.write_to_file")
def test_save_sales_to_local_dir_no_data(mock_write_to_file, mock_makedirs, mock_rmtree, MockSalesClient):
    mock_sales_client = MockSalesClient()
    mock_sales_client.get_sales_transactions.return_value = None

    save_sales_to_local_dir(date="2023-01-01", raw_dir="/tmp/raw_sales", sales_client=mock_sales_client)

    mock_rmtree.assert_called_once_with("/tmp/raw_sales", ignore_errors=True)
    mock_makedirs.assert_called_once_with("/tmp/raw_sales", exist_ok=True)

    assert mock_sales_client.get_sales_transactions.call_count == 1
    mock_sales_client.get_sales_transactions.assert_called_once_with("2023-01-01", 1)

    mock_write_to_file.assert_not_called()


if __name__ == "__main__":
    pytest.main()
