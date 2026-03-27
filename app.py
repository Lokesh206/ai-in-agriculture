from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("krishi.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        password TEXT,
        role TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_id INTEGER,
        crop TEXT,
        weight REAL,
        pickup TEXT,
        destination TEXT,
        vehicle TEXT,
        price REAL,
        status TEXT DEFAULT 'pending',
        transporter_id INTEGER,
        lat REAL DEFAULT 12.9716,
        lng REAL DEFAULT 77.5946
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS bids(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER,
        trader_id INTEGER,
        price REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= HELPERS =================
def is_logged_in():
    return 'user_id' in session

# ================= HOME =================
@app.route('/')
def home():
    return render_template('home.html')

# ================= LOGIN =================
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE phone=? AND password=?",
            (phone, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('select'))

        return render_template('login.html', error="Invalid Credentials")

    return render_template('login.html')

# ================= REGISTER =================
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.form

        role = data['role']
        if role == "transport":
            role = "transporter"

        conn = get_db()
        conn.execute(
            "INSERT INTO users(name, phone, password, role) VALUES (?, ?, ?, ?)",
            (data['name'], data['phone'], data['password'], role)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# ================= SELECT =================
@app.route('/select')
@app.route('/choose-role')
def select():
    if not is_logged_in():
        return redirect(url_for('login'))

    return render_template('selection.html', name=session['name'])

# ================= FARMER =================
@app.route('/farmer')
def farmer():
    if not is_logged_in():
        return redirect(url_for('login'))

    return render_template('farmer.html', name=session['name'])

@app.route('/book', methods=['POST'])
def book():
    data = request.form

    conn = get_db()
    conn.execute("""
    INSERT INTO bookings(farmer_id, crop, weight, pickup, destination, vehicle, price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        session['user_id'],
        data['crop'],
        data['weight'],
        data['pickup'],
        data['destination'],
        data['vehicle'],
        data['price']
    ))
    conn.commit()
    conn.close()

    return redirect(url_for('my_bookings'))

@app.route('/my-bookings')
def my_bookings():
    conn = get_db()
    data = conn.execute(
        "SELECT * FROM bookings WHERE farmer_id=?",
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('my_bookings.html', data=data)

# ================= TRADER =================
@app.route('/trade')
def trade():
    if not is_logged_in():
        return redirect(url_for('login'))

    conn = get_db()
    data = conn.execute("SELECT * FROM bookings WHERE status='pending'").fetchall()
    conn.close()

    return render_template('trade.html', data=data, name=session['name'])

@app.route('/bid/<int:booking_id>', methods=['POST'])
def bid(booking_id):
    price = float(request.form['price'])

    if price <= 0:
        return redirect(url_for('trade'))

    conn = get_db()

    # insert bid
    conn.execute("""
        INSERT INTO bids(booking_id, trader_id, price)
        VALUES (?, ?, ?)
    """, (booking_id, session['user_id'], price))

    # 🔥 IMPORTANT FIX: update booking price
    conn.execute("""
        UPDATE bookings SET price=? WHERE id=?
    """, (price, booking_id))

    conn.commit()
    conn.close()

    return redirect(url_for('trade'))

# ================= ALL BIDS =================
@app.route('/all-bids')
def all_bids():
    if not is_logged_in():
        return redirect(url_for('login'))

    conn = get_db()
    bids = conn.execute("""
        SELECT bids.price, users.name, bookings.crop
        FROM bids
        JOIN users ON bids.trader_id = users.id
        JOIN bookings ON bids.booking_id = bookings.id
    """).fetchall()
    conn.close()

    return render_template('all_bids.html', bids=bids)

# ================= TRANSPORT =================
@app.route('/transport')
def transport():
    if not is_logged_in():
        return redirect(url_for('login'))

    conn = get_db()
    bookings = conn.execute("""
        SELECT * FROM bookings 
        WHERE status='pending' OR status='accepted'
    """).fetchall()
    conn.close()

    return render_template('transporter.html', bookings=bookings, name=session['name'])

@app.route('/accept/<int:id>')
def accept(id):
    if not is_logged_in():
        return redirect(url_for('login'))

    conn = get_db()
    conn.execute("""
    UPDATE bookings
    SET status='accepted', transporter_id=?
    WHERE id=?
    """, (session['user_id'], id))
    conn.commit()
    conn.close()

    return redirect(url_for('transport'))

# ================= TRACK =================
@app.route('/track/<int:id>')
def track(id):
    conn = get_db()
    booking = conn.execute("SELECT * FROM bookings WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template('track.html', booking=booking)

@app.route('/update-location/<int:id>', methods=['POST'])
def update_location(id):
    lat = request.form['lat']
    lng = request.form['lng']

    conn = get_db()
    conn.execute("UPDATE bookings SET lat=?, lng=? WHERE id=?", (lat, lng, id))
    conn.commit()
    conn.close()

    return "OK"

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)