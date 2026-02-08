import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'mydb')
DB_USER = os.environ.get('POSTGRES_USER', 'user')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn


def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS messages (id serial PRIMARY KEY, content varchar(100));')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error init DB: {e}")


with app.app_context():
    init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    container_id = os.uname()[1]

    if request.method == 'POST':
        data = request.json
        content = data.get('content', 'No content')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO messages (content) VALUES (%s)', (content,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({
            "message": "Data saved!",
            "container_id": container_id,
            "saved_content": content
        }), 201

    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM messages;')
        messages = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify({
            "data": messages,
            "served_by_container": container_id
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
