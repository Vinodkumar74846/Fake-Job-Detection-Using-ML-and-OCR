Fake Job Detection using OCR and Flask

This project is a Flask web application that detects whether a job posting is Real or Fake.
Users can either paste job descriptions or upload screenshots of job posts.
The system extracts text using OCR (Tesseract) and checks for suspicious keywords commonly used in job scams.

Features

User Login and Signup system

Upload job posting screenshot

OCR text extraction using Tesseract

Paste job description text

Detect Fake or Real job postings

Shows reasons for fake job detection

Session history of previous predictions

Simple Flask web interface

Technologies Used

Python

Flask

Tesseract OCR

PIL (Python Imaging Library)

HTML / CSS

Regular Expressions

JSON (for storing users)

Project Structure
project-folder
│
├── app.py
├── users.json
├── uploads/
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── upload.html
│   ├── result.html
│   ├── history.html
│   └── about.html
│
└── README.md
Installation
1 Install Python libraries
pip install flask pillow pytesseract
2 Install Tesseract OCR

Download and install:

https://github.com/tesseract-ocr/tesseract

After installation, set the path in the code:

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
3 Run the application
python app.py

Then open:

http://127.0.0.1:5001
How It Works

User logs into the system.

Uploads a job screenshot or pastes a job description.

If an image is uploaded:

OCR extracts the text.

The system scans for suspicious keywords like:

registration fee

urgent hiring

no interview

security deposit

WhatsApp only contact

Based on these indicators, the system predicts:

Fake Job

Real Job

Example Fake Indicators

Asking for registration fees

Immediate hiring without interview

Work from home earn huge money

Contact through WhatsApp only

Security deposit required

Future Improvements

Add Machine Learning model for better accuracy

Add email verification

Deploy the project online

Improve UI design