from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'super secret key'

def get_db_connection():
    conn = psycopg2.connect(
        dbname='mydatabase',
        user='postgres',
        password='',
        host='localhost',
        port='5432'
    )
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE login = %s AND password = %s', (login, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['fio'] = user[1]
            return redirect(url_for('clients'))
        else:
            return 'Неправильный логин или пароль'
    return render_template('login.html')

@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    print(request)
    print(request.form)
    if request.method == 'POST':
        client_id = request.form['client_id']
        new_status = request.form['status']
        cursor.execute('UPDATE clients SET status = %s WHERE id = %s', (new_status, client_id))
        conn.commit()
    cursor.execute('SELECT * FROM clients WHERE responsible_fio = %s', (session['fio'],))
    clients = cursor.fetchall()
    conn.close()
    return render_template('clients.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
