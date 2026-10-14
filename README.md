# Order Summary

This is a simple tool that reads a CSV file of orders and prints:

- the total amount spent by each customer
- the total amount of orders in each month

## What you need

- Python installed on your computer
- A virtual environment set up (folder `env`) with the packages from `requirements.txt` installed

## How to set up (first time only)

1. Open a terminal in this folder (`order-summary`).
2. Create the virtual environment (if not already created):
   ```powershell
   python -m venv env
   ```
3. Activate it:
   ```powershell
   .\env\Scripts\activate
   ```
4. Install the required packages:
   ```powershell
   pip install -r requirements.txt
   ```

## How to run it

Run `main.py` and give it the path to your CSV file:

```powershell
python main.py sample_orders.csv
```

You can replace `sample_orders.csv` with the path to any other CSV file you want to summarize.

## What the CSV file should look like

The file must have these four columns:

| Column    | Meaning                        | Example      |
|-----------|---------------------------------|--------------|
| order_id  | A unique ID for the order       | 101          |
| customer  | Name of the customer            | Anusha Gattu |
| amount    | Order amount (a number)         | 500.00       |
| date      | Date of the order (YYYY-MM-DD)  | 2026-01-10   |

Example:

```csv
order_id,customer,amount,date
101,Anusha Gattu,500.00,2026-01-10
102,Anu,300.00,2026-01-15
```

## Example output

```
=== Total Amount Per Customer ===
Anusha Gattu: 500.00
Anu: 300.00

=== Total Amount Per Month ===
2026-01: 800.00
```

## Running tests

This project has automated tests in the `test` folder (`test/test_main.py`). They check things like:

- totals are calculated correctly
- a clear error shows up if a column is missing
- a clear error shows up if the amount or date is invalid
- a clear error shows up if the file is empty or missing

To run all the tests, go to the `order-summary` folder and run:

```powershell
pytest
```

If everything works, you'll see something like:

```
........                                                                 [100%]
8 passed in 0.06s
```
