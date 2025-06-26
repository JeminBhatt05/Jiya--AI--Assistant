# Import required modules
import mysql.connector
import pandas as pd
from flask import Flask, render_template, request
import os
app = Flask(__name__)

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'port': 3306,
    'password': 'Riddhi@123',
    'database': 'Jemin'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Flask constructor

data_list=[]
# Root endpoint for file upload form
@app.get('/')
def upload():
    return render_template('upload-excel.html')

df=pd.read_excel("jemin_test1.xlsx")
data_list=df.to_dict('records')
id=[]
name=[]
mn=[]
language=[]
gender=[]
for i in data_list:
    id.append(i['id'])
    name.append(i['name'])
    mn.append(i['mn'])
    language.append(i['language'])
    gender.append(i['gender'])



def insert_data():
    
    connection = get_db_connection()
    cursor = connection.cursor()


    for i in data_list:
        datasql=[(i['id'],i['name'],i['mn'],i['language'],i['gender'])]   
        sql="INSERT INTO employe(id,name,mn,language,gender) VALUES (%s,%s,%s,%s,%s)"

        cursor.executemany(sql,datasql)
        connection.commit()
    print("suceess")
insert_data()

# Endpoint to handle uploaded file and display its contents
@app.post('/insert_data')
def view():
    # Get the uploaded file from the request
    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    # Save the file to a temporary location (optional but safer for large files)
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # Read the Excel file into a Pandas DataFrame
    try:
        data = pd.read_excel(filepath)
    except Exception as e:
        return f"Error reading Excel file: {e}"
    
    # Clean up (optional)
    items = ['id', 'name', 'mn', 'language','gender']
    
    os.remove(filepath)
    
    return render_template('upload-excel.html',items=items)
    

@app.route('/submit_selection', methods=['POST'])
def submit_selection():
    selected_value = request.form.get('my_dropdown')
    # 'my_dropdown_name' should match the 'name' attribute of your select tag in HTML
    return f"You selected: {selected_value}"

# @app.route('/insert_data', methods=['POST'])
# def insert_data():
    
#     connection = get_db_connection()
#     cursor = connection.cursor()


#     for i in data_list:
#         datasql=[(i['id'],i['name'],i['mn'],i['language'],i['gender'])]   
#         sql="INSERT INTO employe(id,name,mn,language,gender) VALUES (%s,%s,%s,%s,%s)"

#         cursor.executemany(sql,datasql)
#         connection.commit()
#     print("suceess")
# insert_data()

# Main Driver Function
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
        <br>id:
        

    </form>
    <form action="{{url_for('submit_selection')}}">
        <select name="selected_item" id="selected_item">
            {% for item in items %}
                <option value="{{ item }}" action="{{selected_item}}">{{ item }}</option>
            {% endfor %}
        </select>
        <br>
        name:
        <select name="selected_item1" id="selected_item1">
            {% for item in items %}
                <option value="{{ item }}">{{ item }}</option>
            {% endfor %}
        </select>
        <br>
        mn:
        <select name="selected_item2" id="selected_item2">
            {% for item in items %}
                <option value="{{ item }}">{{ item }}</option>
            {% endfor %}
        </select>
        <br>
        language:
        <select name="selected_item3" id="selected_item3">
            {% for item in items %}
                <option value="{{ item }}">{{ item }}</option>
            {% endfor %}
        </select>
        <br>
        gender:
        <select name="selected_item4" id="selected_item4">
            {% for item in items %}
                <option value="{{ item }}">{{ item }}</option>
            {% endfor %}
        </select>
        <br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>


