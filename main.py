
import argparse
import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED_COLUMNS = {"order_id", "customer", "amount", "date"}


def summarize_orders(file_path):
    """Return total amounts grouped by customer and calendar month."""
    customer_totals = defaultdict(Decimal)
    monthly_totals = defaultdict(Decimal)

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("The CSV file is empty or has no header.")

            missing = REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing:
                raise ValueError(
                    f"Missing required columns: {', '.join(sorted(missing))}"
                )

            for row in reader:
                row_number = reader.line_num

                order_id = (row.get("order_id") or "").strip()
                customer = (row.get("customer") or "").strip()
                amount_text = (row.get("amount") or "").strip()
                date_text = (row.get("date") or "").strip()

                if not all([order_id, customer, amount_text, date_text]):
                    raise ValueError(
                        f"Row ending at line {row_number}: "
                        "all fields must have values."
                    )

                try:
                    amount = Decimal(amount_text)
                    if not amount.is_finite():
                        raise ValueError("Amount must be a finite number.")
                except InvalidOperation:
                    raise ValueError(
                        f"Line {row_number}: invalid amount '{amount_text}'."
                    ) from None

                try:
                    order_date = date.fromisoformat(date_text)
                except ValueError:
                    raise ValueError(
                        f"Line {row_number}: invalid date '{date_text}'. "
                        "Use YYYY-MM-DD."
                    ) from None

                customer_totals[customer] += amount
                month = order_date.strftime("%Y-%m")
                monthly_totals[month] += amount

    except OSError as exc:
        raise ValueError(f"Cannot read '{file_path}': {exc}") from exc

    if not customer_totals:
        raise ValueError("The CSV file contains no orders.")

    return dict(customer_totals), dict(monthly_totals)


def print_report(customer_totals, monthly_totals):
    print("\n=== Total Amount Per Customer ===")
    for customer in sorted(customer_totals):
        print(f"{customer}: {customer_totals[customer]:.2f}")

    print("\n=== Total Amount Per Month ===")
    for month in sorted(monthly_totals):
        print(f"{month}: {monthly_totals[month]:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Summarize order amounts by customer and month."
    )
    parser.add_argument("csv_file", help="Path to the input orders CSV file")
    args = parser.parse_args()

    try:
        customer_totals, monthly_totals = summarize_orders(args.csv_file)
        print_report(customer_totals, monthly_totals)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
