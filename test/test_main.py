from decimal import Decimal

import pytest

from main import summarize_orders


def write_csv(path, content):
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_summarize_orders_basic(tmp_path):
    csv_file = write_csv(
        tmp_path / "orders.csv",
        "order_id,customer,amount,date\n"
        "1,Anu,100.00,2026-01-10\n"
        "2,Anu,50.00,2026-01-20\n"
        "3,Vinny,200.00,2026-02-05\n",
    )

    customer_totals, monthly_totals = summarize_orders(csv_file)

    assert customer_totals == {"Anu": Decimal("150.00"), "Vinny": Decimal("200.00")}
    assert monthly_totals == {"2026-01": Decimal("150.00"), "2026-02": Decimal("200.00")}


def test_missing_required_column(tmp_path):
    csv_file = write_csv(
        tmp_path / "orders.csv",
        "order_id,customer,amount\n1,Anu,100.00\n",
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        summarize_orders(csv_file)


def test_empty_file(tmp_path):
    csv_file = write_csv(tmp_path / "orders.csv", "")

    with pytest.raises(ValueError, match="empty or has no header"):
        summarize_orders(csv_file)


def test_no_orders(tmp_path):
    csv_file = write_csv(
        tmp_path / "orders.csv", "order_id,customer,amount,date\n"
    )

    with pytest.raises(ValueError, match="no orders"):
        summarize_orders(csv_file)


def test_missing_value_in_row(tmp_path):
    csv_file = write_csv(
        tmp_path / "orders.csv",
        "order_id,customer,amount,date\n1,Anu,,2026-01-10\n",
    )

    with pytest.raises(ValueError, match="all fields must have values"):
        summarize_orders(csv_file)


def test_invalid_amount(tmp_path):
    csv_file = write_csv(
        tmp_path / "orders.csv",
        "order_id,customer,amount,date\n1,Anu,not-a-number,2026-01-10\n",
    )

    with pytest.raises(ValueError, match="invalid amount"):
        summarize_orders(csv_file)


def test_invalid_date(tmp_path):
    csv_file = write_csv(
        tmp_path / "orders.csv",
        "order_id,customer,amount,date\n1,Anu,100.00,10-01-2026\n",
    )

    with pytest.raises(ValueError, match="invalid date"):
        summarize_orders(csv_file)


def test_file_not_found():
    with pytest.raises(ValueError, match="Cannot read"):
        summarize_orders("does_not_exist.csv")
