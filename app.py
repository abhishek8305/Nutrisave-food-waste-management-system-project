from flask import Flask, render_template, request, redirect, session,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"
@app.route("/")
def home():
    return redirect(url_for("login"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("SELECT role FROM users WHERE email=? AND password=?",
                    (email, password))

        user = cur.fetchone()
        conn.close()

        if user:
            role = user[0]
            session["user"] = email
            session["role"] = role

            if role == "restaurant":
                return redirect(url_for("restaurant_dashboard"))
            else:
                return redirect(url_for("ngo_dashboard"))
        else:
            return "Invalid Login"

    return render_template("login.html")


# ---------------- RESTAURANT DASHBOARD ----------------
@app.route("/restaurant_dashboard")
def restaurant_dashboard():
    if session.get("role") != "restaurant":
        return redirect(url_for("login"))

    return render_template("restaurant_dashboard.html")


@app.route('/add_food', methods=['POST'])
def add_food():
    food_name = request.form['food_name']
    quantity = request.form['quantity']
    location = request.form['location']

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO food (food_name, quantity, location) VALUES (?, ?, ?)",
        (food_name, quantity, location)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('restaurant_dashboard'))

# ---------------- NGO DASHBOARD ----------------
@app.route("/ngo_dashboard")
def ngo_dashboard():
    if session.get("role") != "ngo":
        return redirect(url_for("login"))
    return render_template("ngo_dashboard.html")


# ---------------- AVAILABLE FOOD ----------------
@app.route("/available_food")
def available_food():
    if session.get("role") != "ngo":
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT id,food_name, quantity, location FROM food")
    foods = cur.fetchall()

    conn.close()

    return render_template("available_food.html", foods=foods)
@app.route('/accept_food/<int:id>')
def accept_food(id):
    import sqlite3

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()


    food = cur.execute("SELECT * FROM food WHERE id=?", (id,)).fetchone()

    cur.execute("""
        INSERT INTO requests (name, quantity, location, status)
        VALUES (?, ?, ?, ?)
    """, (food[1], food[2], food[3], "Accepted"))
    
    cur.execute("delete from food where id=?",(id,))
    

    conn.commit()
    conn.close()

    return redirect('/available_food')

@app.route('/my_requests')
def my_requests():
    import sqlite3

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    requests = cur.execute("SELECT * FROM requests").fetchall()

    conn.close()
    return render_template("my_requests.html", requests=requests)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
 session.pop("user", None)
 session.pop("role", None)
 return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
  
     
     
     
     