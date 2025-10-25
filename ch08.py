
import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Excel file path
EXCEL_FILE = os.path.join(os.path.dirname(__file__), 'stock.xls')

def read_data():
    try:
        df = pd.read_excel(EXCEL_FILE)
        # Replace NaN with empty strings for display
        df = df.fillna('')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def write_data(df):
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def index():
    df = read_data()
    if df.empty:
        return "Excel file not found or is empty. Please create 'stock.xls'.", 404

    # Add an index for editing/deleting if not present
    if 'id' not in df.columns:
        df['id'] = range(len(df))

    # Search
    search_query = request.args.get('search', '')
    if search_query:
        # Searches all columns for the query
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    # Sorting
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Items per page
    total_rows = len(df)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_df = df.iloc[start:end]

    total_pages = (total_rows + per_page - 1) // per_page

    return render_template('index.html', 
                           records=paginated_df.to_dict('records'),
                           page=page,
                           total_pages=total_pages,
                           sort_by=sort_by,
                           sort_order=sort_order,
                           search_query=search_query,
                           columns=df.columns)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        df = read_data()
        
        # Create a new record from form data
        new_record = {}
        for col in df.columns:
            if col != 'id': # Don't manually set the id
                new_record[col] = request.form[col]
        
        # Append new record
        new_df = pd.DataFrame([new_record])
        df = pd.concat([df, new_df], ignore_index=True)

        write_data(df)
        return redirect(url_for('index'))
    
    # For GET request, show the form
    df = read_data()
    return render_template('add.html', columns=df.columns)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    df = read_data()
    
    # Ensure 'id' column exists for safe indexing
    if 'id' not in df.columns:
        df['id'] = range(len(df))

    # Find the record to edit
    record_to_edit = df[df['id'] == id]

    if record_to_edit.empty:
        return "Record not found", 404

    if request.method == 'POST':
        # Update the record
        for col in df.columns:
            if col != 'id':
                df.loc[df['id'] == id, col] = request.form[col]
        
        write_data(df)
        return redirect(url_for('index'))

    return render_template('edit.html', record=record_to_edit.to_dict('records')[0], id=id)

@app.route('/delete/<int:id>')
def delete(id):
    df = read_data()
    
    if 'id' not in df.columns:
        df['id'] = range(len(df))

    # Drop the record by id
    df = df[df['id'] != id]
    
    write_data(df)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
