from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="hr_user",
    password="Food2025!",
    database="hr_db"
)

cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get data from form
        first = request.form.get("first_name")
        last = request.form.get("last_name")
        if first and last:
            cursor.execute("INSERT INTO employees (first_name, last_name) VALUES (%s, %s)", (first, last))
            db.commit()

    # Fetch all employees
    cursor.execute("SELECT first_name, last_name FROM employees")
    employees = cursor.fetchall()
    employee_list = "<ul>" + "".join([f"<li>{first} {last}</li>" for first, last in employees]) + "</ul>"

    return f"""
    <html>
        <head>
            <title>HR Employees</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    text-align: center;
                    padding: 50px;
                }}
                h1 {{
                    color: #2c3e50;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                li {{
                    background-color: #fff;
                    margin: 10px auto;
                    padding: 15px 25px;
                    max-width: 400px;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                }}
                li:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                }}
                form {{
                    margin-top: 30px;
                }}
                input[type=text] {{
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    width: 200px;
                }}
                input[type=submit] {{
                    padding: 10px 20px;
                    margin-top: 10px;
                    background-color: #2c3e50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                input[type=submit]:hover {{
                    background-color: #34495e;
                }}
            </style>
        </head>
        <body>
            <h1>HR Employees</h1>
            {employee_list}
            <form method="POST">
                <input type="text" name="first_name" placeholder="First Name" required>
                <input type="text" name="last_name" placeholder="Last Name" required>
                <br>
                <input type="submit" value="Add Employee">
            </form>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
