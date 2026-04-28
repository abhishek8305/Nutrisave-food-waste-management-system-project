from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect(url_for("login"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]   

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM users
            WHERE email=? AND password=? AND role=?
        """, (email, password, role))

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = email
            session["role"] = role

            if role == "restaurant":
                return redirect(url_for("restaurant_dashboard"))
            elif role == "ngo":
                return redirect(url_for("ngo_dashboard"))
            elif role == "admin":
                return redirect(url_for("admin"))
        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print("FORM RECEIVED")  

        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (email, password, role)
            VALUES (?, ?, ?)
        """, (email, password, role))

        conn.commit()
        conn.close()

        print("SAVED TO DB:", email, password, role)

        return redirect(url_for("login"))

    return render_template("signup.html")
# ---------------- RESTAURANT DASHBOARD ----------------
@app.route("/restaurant_dashboard")
def restaurant_dashboard():
    if session.get("role") != "restaurant":
        return redirect(url_for("login"))

    return render_template("restaurant_dashboard.html")


# ---------------- ADD FOOD ----------------
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

# ---------------- MY FOOD (Restaurant) ----------------
@app.route("/my_food")
def my_food():
    if session.get("role") != "restaurant":
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # sirf food table ka data
    cur.execute("SELECT id, food_name, quantity, location FROM food")
    foods = cur.fetchall()

    conn.close()

    return render_template("my_food.html", foods=foods)

# ---------------- DONATION STATUS ----------------
@app.route("/donation_status")
def donation_status():

    if session.get("role") != "restaurant":
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT id, name, quantity, location, status FROM requests")
    data = cur.fetchall()

    conn.close()

    return render_template("donation_status.html", data=data)

@app.route("/overview")
def overview():
    if session.get("role") != "restaurant":
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # Total food
    cur.execute("SELECT COUNT(*) FROM food")
    total_food = cur.fetchone()[0]

    # Total requests
    cur.execute("SELECT COUNT(*) FROM requests")
    total_requests = cur.fetchone()[0]

    # Accepted
    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Accepted'")
    accepted = cur.fetchone()[0]

    # Pending
    cur.execute("SELECT COUNT(*) FROM requests WHERE status='Pending'")
    pending = cur.fetchone()[0]

    conn.close()

    return render_template("overview.html",
                           total_food=total_food,
                           total_requests=total_requests,
                           accepted=accepted,
                           pending=pending)
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

    cur.execute("SELECT id, food_name, quantity, location FROM food")
    foods = cur.fetchall()

    conn.close()

    return render_template("available_food.html", foods=foods)


# ---------------- ACCEPT FOOD ----------------
@app.route('/accept_food/<int:id>')
def accept_food(id):

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    food = cur.execute(
        "SELECT * FROM food WHERE id=?",
        (id,)
    ).fetchone()

    if food:
        cur.execute(
            "INSERT INTO requests (name, quantity, location, status) VALUES (?, ?, ?, ?)",
            (food[1], food[2], food[3], "Accepted")
        )

        cur.execute("DELETE FROM food WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/available_food')


# ---------------- MY REQUESTS ----------------
@app.route('/my_requests')
def my_requests():

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    requests = cur.execute("SELECT * FROM requests").fetchall()

    conn.close()

    return render_template("my_requests.html", requests=requests)


# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM food")
    food = cur.fetchall()

    cur.execute("SELECT * FROM requests")
    requests = cur.fetchall()

    conn.close()

    return render_template("admin.html",
                           users=users,
                           food=food,
                           requests=requests)


# ---------------- DELETE USER ----------------
@app.route("/delete_user/<int:id>")
def delete_user(id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")


# ---------------- DELETE FOOD ----------------
@app.route("/delete_food/<int:id>")
def delete_food(id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM food WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")


# ---------------- UPDATE REQUEST ----------------
@app.route("/update_request/<int:id>/<status>")
def update_request(id, status):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("UPDATE requests SET status=? WHERE id=?", (status, id))
    conn.commit()

@app.route("/help")
def help():
    return render_template("help.html")



# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)