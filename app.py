from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient, errors
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb+srv://admin:mayur123@cyberhunter.h1bcf.mongodb.net/?retryWrites=true&w=majority&appName=CyberHunter"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    client.server_info()  # Forces a call to check connection
    db = client['java_lab']
    collection = db['submissions']
except errors.ServerSelectionTimeoutError as err:
    print("MongoDB connection failed:", err)
    collection = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not collection:
        return jsonify({"success": False, "error": "Database not connected"}), 500

    student_name = request.form.get('student_name')
    class_name = request.form.get('class_name')
    roll_number = request.form.get('roll_number')

    if not student_name or not class_name or not roll_number:
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    submission = {
        'name': student_name.strip(),
        'class': class_name.strip(),
        'roll_number': roll_number.strip(),
        'timestamp': datetime.utcnow()
    }

    try:
        collection.insert_one(submission)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/download_zip1')
def download_zip1():
    path = "Advance_Java_Lab_Manual.rar"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@app.route('/download_zip2')
def download_zip2():
    path = "AJP_Final_Codes.rar"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
