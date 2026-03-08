from flask import Flask, request, render_template, session, redirect, url_for
import os
from PIL import Image
import pytesseract
import re
import logging
import json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'some_random_string'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

USERS_FILE = "users.json"

# Load users from file or set default admin
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            'admin': {'phone': '9999999999', 'password': 'password'}
        }

# Save users to file
def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(USERS, f)

# Initialize users
USERS = load_users()


def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')
    return img

def extract_text_from_image(image_path):
    try:
        img = preprocess_image(image_path)
        text = pytesseract.image_to_string(img)
        if not text.strip():
            return "Error: No text detected in the image."
        return text
    except Exception as e:
        logging.error(f"OCR error: {str(e)}")
        return f"Error extracting text: {str(e)}"

def clean_text(text):
    text = re.sub(r'[^\w\s.,@\u20B9\-()]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def predict_job_posting(text):
    text_lower = text.lower()
    red_flags = {
        "urgent hiring": "Creates urgency, common in fake job scams.",
        "no experience needed": "Too good to be true for high-paying jobs.",
        "registration fee": "Asking for money to apply is a scam indicator.",
        "pay to apply": "Genuine jobs don’t require payments.",
        "immediate hiring": "Used to rush people into scams.",
        "refund after joining": "Fake jobs often promise to refund money after you pay.",
        "work from home and earn": "Vague and overpromising.",
        "whatsapp only": "Scammers often use WhatsApp only.",
        "sms verification job": "Sounds suspiciously fake.",
        "security deposit": "Legitimate jobs never ask for this.",
        "no interview": "Real jobs usually have at least one interview.",
        "just fill forms": "Not a real role.",
        "\u20B9": "Currency signs in job ads are red flags when overused.",
        "company does not exist": "No official presence for the company online.",
        "role not found on official website": "Job post is not listed on official company careers page.",
        "suspicious email domain": "Personal email domain like gmail or yahoo used.",
        "unprofessional language": "Poor grammar and spelling indicates a lack of professionalism.",
        "contact via whatsapp": "Communicating solely via WhatsApp is unusual for legit employers.",
        "refundable deposit": "Mentions of refundable training fees are red flags."
    }
    reasons = [reason for keyword, reason in red_flags.items() if keyword in text_lower]
    return {"prediction": "Fake" if reasons else "Real", "reasons": reasons}


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('upload_form'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('upload_form'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html', error=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if username in USERS:
            return render_template('signup.html', error="Username already exists")
        if password != confirm:
            return render_template('signup.html', error="Passwords do not match")
        if not username or not phone or not password:
            return render_template('signup.html', error="All fields are required")

        USERS[username] = {'phone': phone, 'password': password}
        save_users()
        return redirect(url_for('login'))

    return render_template('signup.html', error=None)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload')
def upload_form():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    pasted_text = request.form.get('job_description', '').strip()
    file = request.files.get('file')
    image_path = None
    extracted_text = None

    if file and file.filename != '':
        try:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)
            extracted_text = extract_text_from_image(image_path)
            if "Error" in extracted_text or not extracted_text:
                return render_template('result.html', prediction=extracted_text, source="Screenshot", processed_text="", reasons=[])
        except Exception as e:
            return render_template('result.html', prediction=f"Error processing file: {str(e)}", source="Screenshot", processed_text="", reasons=[])

    if extracted_text:
        source = "Screenshot"
        text_to_process = extracted_text
    elif pasted_text:
        source = "Pasted Text"
        text_to_process = pasted_text
    else:
        return "No input provided.", 400

    cleaned_text = clean_text(text_to_process)
    if len(cleaned_text.split()) < 5:
        return render_template('result.html', prediction="Error: Text too short.", source=source, processed_text=cleaned_text, reasons=[])

    prediction_result = predict_job_posting(cleaned_text)

    if 'history' not in session:
        session['history'] = []
    session['history'].append({
        'source': source,
        'processed_text': cleaned_text,
        'prediction': prediction_result['prediction']
    })
    session.modified = True

    return render_template('result.html', prediction=prediction_result['prediction'], reasons=prediction_result['reasons'], source=source, processed_text=cleaned_text)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('history.html', history=session.get('history', []))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
