from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        ''')
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cars", methods=["GET", "POST"])
def cars():
    if request.method == "POST":
        data = request.json
        make = data.get("make")
        model = data.get("model")
        year = data.get("year")
        
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cars (make, model, year) VALUES (?, ?, ?)",
                (make, model, year),
            )
            conn.commit()
        return jsonify({"message": "Автомобіль додано!"}), 201

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        cars = [{"id": row[0], "make": row[1], "model": row[2], "year": row[3]} for row in cursor.fetchall()]
    return jsonify(cars)

@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        conn.commit()
    return jsonify({"message": "Автомобіль видалено!"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
