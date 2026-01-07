from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database='mydb',
        user='user',
        password='password'
    )
    return conn

@app.route('/')
def index():
    container_id = os.uname()[1]
    return jsonify({
        "message": "hello from backend side",
        "container_id": container_id
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)