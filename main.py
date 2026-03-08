from flask import Flask, request, render_template, session, redirect, url_for
import os
from PIL import Image
import pytesseract
import re
import logging
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ----------------- Logging -----------------
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# ----------------- Flask Setup -----------------
app = Flask(__name__)
app.secret_key = 'some_random_string'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------- Tesseract OCR Setup -----------------
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ----------------- User Storage (Demo) -----------------
USERS = {
    'admin': {'phone': '9999999999', 'password': 'password'}
}

# ----------------- Load Model + Tokenizer -----------------
MODEL_PATH = "fake_job_lstm_model.h5"
TOKENIZER_PATH = "tokenizer.pkl"
MAX_SEQUENCE_LENGTH = 300   # use same as during training

model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)

# ----------------- Helper Functions -----------------
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

def preprocess_for_model(text):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
    return padded

def predict_job_posting(text):
    # Predict with LSTM model
    processed = preprocess_for_model(text)
    prob = model.predict(processed)[0][0]  # binary classification
    prediction = "Fake" if prob > 0.5 else "Real"

    # Optional keyword-based explanations
    text_lower = text.lower()
    red_flags = {
        "registration fee": "Asking for money is a scam indicator.",
        "pay to apply": "Genuine jobs don’t require payment.",
        "urgent hiring": "Creates urgency, common in fake scams.",
        "whatsapp only": "Legitimate companies don’t recruit only on WhatsApp.",
        "no interview": "Most real jobs have an interview process.",
        "security deposit": "Legit employers never ask for deposits."
    }
    reasons = [reason for keyword, reason in red_flags.items() if keyword in text_lower]

    return {"prediction": prediction, "probability": float(prob), "reasons": reasons}

# ----------------- Routes -----------------
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
                return render_template('result.html', prediction=extracted_text, source="Screenshot", processed_text="", reasons=[], probability=None)
        except Exception as e:
            return render_template('result.html', prediction=f"Error processing file: {str(e)}", source="Screenshot", processed_text="", reasons=[], probability=None)

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
        return render_template('result.html', prediction="Error: Text too short.", source=source, processed_text=cleaned_text, reasons=[], probability=None)

    prediction_result = predict_job_posting(cleaned_text)

    # Save to history
    if 'history' not in session:
        session['history'] = []
    session['history'].append({
        'source': source,
        'processed_text': cleaned_text,
        'prediction': prediction_result['prediction'],
        'probability': prediction_result['probability']
    })
    session.modified = True

    return render_template(
        'result.html',
        prediction=prediction_result['prediction'],
        reasons=prediction_result['reasons'],
        probability=round(prediction_result['probability'] * 100, 2),
        source=source,
        processed_text=cleaned_text
    )

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('history.html', history=session.get('history', []))

@app.route('/about')
def about():
    return render_template('about.html')

# ----------------- Run -----------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
