from flask import Flask, render_template, request, send_file
from docx import Document
import io
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Replace with your MongoDB Atlas connection string
client = MongoClient("mongodb+srv://mayurtamanke:mayur123#@cyberhunterdb.dr09i.mongodb.net/?retryWrites=true&w=majority&tls=true")
db = client['assignment_db']  # Database name
collection = db['downloads']  # Collection name

def replace_placeholders_in_docx(name, class_name, roll_number):
    doc = Document("assignment.docx")
    for paragraph in doc.paragraphs:
        if 'xyz' in paragraph.text:
            paragraph.text = paragraph.text.replace('xyz', name)
        if 'classssss' in paragraph.text:
            paragraph.text = paragraph.text.replace('classssss', class_name)
        if '11111111' in paragraph.text:
            paragraph.text = paragraph.text.replace('11111111', roll_number)

    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    
    return doc_io

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    student_name = request.form['student_name']
    class_name = request.form['class_name']
    roll_number = request.form['roll_number']
    
    download_entry = {
        "student_name": student_name,
        "class_name": class_name,
        "roll_number": roll_number,
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(download_entry)
    
    updated_docx = replace_placeholders_in_docx(student_name, class_name, roll_number)
    
    return send_file(
        updated_docx,
        as_attachment=True,
        download_name=f"assignment_{student_name}.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
