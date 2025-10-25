# Stock Management Web Application

This is a simple web application for managing stock data stored in an Excel file (`stock.xls`).

## Features

- **CRUD Operations:** Create, Read, Update, and Delete stock records.
- **Web Interface:** Provides a user-friendly web interface to interact with the data.
- **Search:** Search for specific data across all columns.
- **Sorting:** Sort data by any column in ascending or descending order.
- **Pagination:** Data is paginated for better readability.

## Technologies Used

- **Backend:** Python, Flask
- **Data Manipulation:** Pandas
- **Frontend:** HTML (using Flask templates)

## How to Run

1.  Make sure you have Python, Flask, and Pandas installed.
    ```bash
    pip install Flask pandas openpyxl
    ```
2.  Run the application:
    ```bash
    python ch08.py
    ```
3.  Open your web browser and go to `http://127.0.0.1:5000`.
