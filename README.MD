# 🚨 Fake Job Detection System using OCR & Flask

## 📌 Project Overview
The **Fake Job Detection System** is a Flask-based web application that helps users identify whether a job posting is **Real ✅ or Fake ❌**.

Users can either:
- 📄 **Paste a job description**
- 🖼 **Upload a screenshot of a job post**

The system extracts text using **Tesseract OCR** and analyzes the content to detect **suspicious patterns commonly found in job scams**.

---

# ✨ Features

🔐 **User Authentication**
- Login and Signup system

🖼 **Image Upload**
- Upload job post screenshots

🔎 **OCR Text Extraction**
- Extracts text from images using **Tesseract OCR**

📄 **Text Input**
- Users can paste job descriptions directly

🤖 **Fake Job Detection**
- Detects suspicious keywords used in scams

📊 **Prediction Result**
- Shows whether the job is **Fake or Real**

📜 **Detection Reasons**
- Displays the reasons for classification

📚 **History Tracking**
- Stores previous predictions in session history

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Backend Development |
| 🌐 Flask | Web Framework |
| 🔎 Tesseract OCR | Text Extraction from Images |
| 🖼 PIL (Pillow) | Image Processing |
| 📄 HTML / CSS | Frontend Interface |
| 📂 JSON | User Data Storage |

---

# 📂 Project Structure

```
fake-job-detection
│
├── app.py
├── users.json
├── README.md
│
├── uploads/
│
└── templates/
    ├── login.html
    ├── signup.html
    ├── upload.html
    ├── result.html
    ├── history.html
    └── about.html
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/fake-job-detection.git
```

```
cd fake-job-detection
```

---

## 2️⃣ Install Required Libraries

```bash
pip install flask pillow pytesseract
```

---

## 3️⃣ Install Tesseract OCR

Download and install Tesseract:

🔗 https://github.com/tesseract-ocr/tesseract

After installation, update the path in the code:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 4️⃣ Run the Application

```bash
python app.py
```

Then open your browser:

```
http://127.0.0.1:5001
```

---

# ⚡ How It Works

1️⃣ User logs into the system 🔐  
2️⃣ Uploads a **job screenshot** or pastes **job description text** 📄  
3️⃣ If an image is uploaded, **OCR extracts the text** 🔎  
4️⃣ The system scans the text for **suspicious keywords** ⚠️  
5️⃣ Based on the analysis, the system predicts:

- ✅ **Real Job**
- ❌ **Fake Job**

---

# 🚩 Common Fake Job Indicators

⚠️ **Registration Fee Required**  
⚠️ **Immediate Hiring Without Interview**  
⚠️ **Work From Home & Earn Huge Money**  
⚠️ **WhatsApp Only Communication**  
⚠️ **Security Deposit Required**  
⚠️ **Refundable Training Fees**

These indicators are commonly used in **online job scams**.

---

# 🚀 Future Improvements

✨ Integrate **Machine Learning Model**  
✨ Improve **User Interface Design**  
✨ Add **Email Verification System**  
✨ Deploy the application to **Cloud Platform**

---

# 👨‍💻 Author

**Vinod Kumar**  
🎓 MCA Student  
🏫 Aurora Deemed to be University

---

# ⭐ Support

If you like this project, please consider giving it a **⭐ Star on GitHub**.