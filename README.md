# StudyMate AI

**StudyMate AI** adalah chatbot pembelajaran berbasis LLM yang dapat membantu mahasiswa memahami materi, membuat ringkasan, dan berlatih melalui quiz.

Project ini dibuat sebagai Final Project untuk training **LLM-Based Tools and Gemini API Integration for Data Scientists**.

## ✨ Fitur

- 💬 Chatbot berbasis Gemini API
- 🧠 Konteks percakapan / chat history
- 🗣️ Bisa pilihan gaya bahasa:
  - Sederhana
  - Santai
  - Formal
- 🎯 Mode belajar:
  - Penjelasan
  - Ringkasan
  - Quiz
- 🌡️ Pengaturan tingkat temprature
- 🗑️ Tombol untuk menghapus percakapan
- 🌐 User interface berbasis Streamlit

## 🏗️ Arsitektur

```text
User
  ↓
Streamlit UI
  ↓
Prompt + Chat History
  ↓
Gemini API
  ↓
Gemini LLM
  ↓
Response
  ↓
Streamlit UI
```

## 🛠️ Teknologi

- Python
- Streamlit
- Google Gemini API
- `google-genai` Python SDK

## 🚀 Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/USERNAME/StudyMate-AI.git
cd StudyMate-AI
```

### 2. Buat virtual environment (opsional tetapi disarankan)

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependency

```bash
pip install -r requirements.txt
```

### 4. Siapkan API key

Buat file `.env` dari `.env.example`.

Isi:

```env
GEMINI_API_KEY=-------- (Menggunakan API key Gemini)
GEMINI_MODEL=gemini-3.8-flash
```

### 5. Jalankan aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser.

## 📌 Final Project

Use case:
**Education / Personal Learning Assistant**

Parameter kreatif:
- Gaya bahasa
- Mode belajar
- Temperature / tingkat kreativitas
- Memory percakapan

Deliverables:
- URL repository GitHub
- Screenshot User Interface
