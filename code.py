from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
import os

app = Flask(__name__)



#connection for database of mysql 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'port': 3306,
    'password': 'Riddhi@123',
    'database': 'Jemin'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


uploaded_data = pd.DataFrame()
items = ['', 'id', 'name', 'mn', 'language', 'gender']



@app.route('/')
def upload():
    return render_template('select1.html', items=items)

@app.post('/view')
def view():
    global uploaded_data

    file = request.files['file']
    if file.filename == '':
        return "No file selected."

    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        uploaded_data = pd.read_excel(filepath)
    except Exception as e:
        return f"Error reading Excel file: {e}"
    finally:
        os.remove(filepath)

    return render_template('select1.html', items=items, success="File uploaded successfully. Now select the mappings.")

@app.route('/submit_selection', methods=['POST'])
def submit_selection():
    global uploaded_data

    if uploaded_data.empty:
        return render_template('select1.html', items=items, error="No data found. Please upload an Excel file first.")

    selections = [
        request.form.get('selected_item'),
        request.form.get('selected_item1'),
        request.form.get('selected_item2'),
        request.form.get('selected_item3'),
        request.form.get('selected_item4'),
    ]
    connection = get_db_connection()
    cursor = connection.cursor()
    if 'item1' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (id);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item2' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (name);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item3' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (mn);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item4' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (language);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    elif 'item5' in request.form:
        sql="ALTER TABLE employe ADD UNIQUE (gender);"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    if len(selections) != len(set(selections)):
        return render_template('select1.html', items=items, error="Please select different columns for each field.")

    try:
        store(*selections)
        return render_template('select1.html', items=items, success="Data inserted successfully.")
    except Exception as e:
        return render_template('select1.html', items=items, error=f"Error inserting data: {e}")

a1=[]
a2=[]
a3=[]
a4=[]
a5=[]
b1=[]
b2=[]
b3=[]
b4=[]
b5=[]





def insert_data(data_list):
    connection = get_db_connection()
    cursor = connection.cursor()
    # query = "SELECT * FROM employe"

    # # Fetch data into a DataFrame
    # df = pd.read_sql(query, cursor)
    # my_dict=df.to_dict('records')
        
    sql = "INSERT INTO employe(id, name, mn, language, gender) VALUES (%s, %s, %s, %s, %s)"
    values = [(i['id'], i['name'], i['mn'], i['language'], i['gender']) for i in data_list]
    cursor.executemany(sql, values)
    connection.commit()
    cursor.close()
    connection.close()

def store(s, s1, s2, s3, s4):
    global uploaded_data
    # connection = get_db_connection()
    # cursor = connection.cursor()
    # query = "SELECT * FROM employe"

    # # Fetch data into a DataFrame
    # df = pd.read_sql(query, cursor)
    # my_dict=df.to_dict('records')
    # for i in data_list:
    #     a1.append(i['id'])
    #     a2.append(i['name'])
    #     a3.append(i['mn'])
    #     a4.append(i['language'])
    #     a5.append(i['gender'])
    # for i in my_dict:
    #     b1.append(i['id'])
    #     b2.append(i['name'])
    #     b3.append(i['mn'])
    #     b4.append(i['language'])
    #     b5.append(i['gender'])
    mapping = {'id': s, 'name': s1, 'mn': s2, 'language': s3, 'gender': s4}
    renamed_df = uploaded_data[[v for v in mapping.values()]].copy()
    renamed_df.columns = list(mapping.keys())
    data_list = renamed_df.to_dict(orient='records')
    insert_data(data_list)


if __name__ == '__main__':
    app.run(debug=True)





<!DOCTYPE html>
<html>
<head>
    <title>Upload Excel</title>
    

</head>
<body>
    <h2>Upload an Excel File</h2>
    <form action="{{ url_for('view') }}" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xls,.xlsx" required>
        <input type="submit" value="Upload">
    </form>

    <form id="selectionForm" action="{{ url_for('submit_selection') }}" method="POST" onsubmit="return validateSelection()">
        id:
        <select name="selected_item" id="selected_item">
            {% for item in items %}
            <option value="{{ item }}" {% if item == selected_value %}disabled{% endif %}>{{ item }}</option>
            {% endfor %}
        </select><input type="checkbox" id="item1" name="item1" value="selected_item">Set Unique
        <br>
        
        name:
        <select name="selected_item1" id="selected_item1">
            {% for item in items %}
            <option value="{{ item }}" {% if item == selected_value %}disabled{% endif %}>{{ item }}</option>
            {% endfor %}
        </select><input type="checkbox" id="item2" name="item2" value="selected_item1">Set Unique
        <br>

        mn:
        <select name="selected_item2" id="selected_item2">
            {% for item in items %}
            <option value="{{ item }}" {% if item == selected_value %}disabled{% endif %}>{{ item }}</option>
            {% endfor %}
        </select><input type="checkbox" id="item3" name="item3" value="selected_item2">Set Unique<br>

        language:
        <select name="selected_item3" id="selected_item3">
            {% for item in items %}
            <option value="{{ item }}" {% if item == selected_value %}disabled{% endif %}>{{ item }}</option>
            {% endfor %}
        </select><input type="checkbox" id="item4" name="item4" value="selected_item3">Set Unique<br>

        gender:
        <select name="selected_item4" id="selected_item4">
            {% for item in items %}
            <option value="{{ item }}" {% if item == selected_value %}disabled{% endif %}>{{ item }}</option>
            {% endfor %}
        </select><input type="checkbox" id="item5" name="item5" value="selected_item4">Set Unique<br>

        <button type="submit">Submit</button>
    </form>

    <script type="text/javascript">
        function validateSelection() {
            const selectedValue = document.getElementById("selected_item").value;
            const selectedValue1 = document.getElementById("selected_item1").value;
            const selectedValue2 = document.getElementById("selected_item2").value;
            const selectedValue3 = document.getElementById("selected_item3").value;
            const selectedValue4 = document.getElementById("selected_item4").value;

            const selectedValues = [selectedValue, selectedValue1, selectedValue2, selectedValue3, selectedValue4];
            const hasDuplicates = new Set(selectedValues).size !== selectedValues.length;

            if (hasDuplicates) {
                alert("Please select different values for each field.");
                return false; //form submission nai tahava dei
            }

            return true; //for form submission
        }
    </script>
</body>
</html>
