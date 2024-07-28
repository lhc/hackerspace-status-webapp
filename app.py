from flask import Flask, render_template, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'logs.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      event TEXT NOT NULL, 
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 5')
    logs = cursor.fetchall()
    cursor.execute('SELECT event FROM logs ORDER BY timestamp DESC LIMIT 1')
    current_status = cursor.fetchone()
    conn.close()
    if current_status:
        current_status = current_status[0]
    else:
        current_status = 'LHC Fechado'
    return render_template('index.html', logs=logs, current_status=current_status)

@app.route('/lhc_aberto')
def lhc_aberto():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (event) VALUES ('LHC Aberto')")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/lhc_fechado')
def lhc_fechado():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (event) VALUES ('LHC Fechado')")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/status/lhc')
def api_status_lhc():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 1')
    log = cursor.fetchone()
    conn.close()
    if log:
        response = {
            'id': log[0],
            'event': log[1],
            'timestamp': log[2]
        }
    else:
        response = {
            'message': 'No logs found'
        }
    return jsonify(response)

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", debug=True)
