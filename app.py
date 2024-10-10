from flask import Flask, render_template, request, send_file
from docx import Document
import io

app = Flask(__name__)

# Function to replace 'xyz' with student's name in the docx file
def replace_name_in_docx(name):
    # Load the existing assignment.docx
    doc = Document("assignment.docx")
    
    # Replace 'xyz' placeholder with the student's name
    for paragraph in doc.paragraphs:
        if 'xyz' in paragraph.text:
            paragraph.text = paragraph.text.replace('xyz', name)

    # Save the modified document to a BytesIO object for download
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
    
    # Generate the modified docx file
    updated_docx = replace_name_in_docx(student_name)
    
    # Send the modified document as a download
    return send_file(updated_docx, as_attachment=True, download_name=f"assignment_{student_name}.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

