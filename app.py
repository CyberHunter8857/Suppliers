from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb+srv://admin:mayur123@cyberhunter.h1bcf.mongodb.net/?retryWrites=true&w=majority&appName=CyberHunter")
db = client['java_lab']
collection = db['submissions']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    student_name = request.form['student_name']
    class_name = request.form['class_name']
    roll_number = request.form['roll_number']

    submission = {
        'name': student_name,
        'class': class_name,
        'roll_number': roll_number,
        'timestamp': datetime.utcnow()
    }
    collection.insert_one(submission)

    # Respond with success
    return jsonify({"success": True})

@app.route('/download_zip1')
def download_zip1():
    return send_file("Advance_Java_Lab_Manual.rar", as_attachment=True)

@app.route('/download_zip2')
def download_zip2():
    return send_file("AJP_Final_Codes.rar", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
