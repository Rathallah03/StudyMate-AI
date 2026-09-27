import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="centered",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        color: #6b7280;
        margin-bottom: 1.2rem;
    }
    .feature-card {
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,.2);
        background: rgba(128,128,128,.05);
        margin-bottom: .6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Configuration ----------
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Pengaturan")

    style = st.selectbox(
        "🗣️ Gaya Bahasa",
        ["Sederhana", "Santai", "Formal"],
        index=0,
    )

    mode = st.selectbox(
        "🎯 Mode Belajar",
        ["Penjelasan", "Ringkasan", "Quiz"],
        index=0,
    )

    temperature = st.slider(
        "🌡️ Kreativitas",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Semakin tinggi, jawaban cenderung lebih variatif.",
    )

    st.divider()

    if st.button("🗑️ Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("🤖 Model")
    st.code(MODEL_NAME, language="text")
    st.caption("📚 StudyMate AI")
    st.caption("AI Learning Assistant")

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Halo! 👋 Saya **StudyMate AI**, asisten belajar berbasis Gemini. "
                "Tanyakan materi yang ingin kamu pahami, minta rangkuman, atau mulai quiz."
            ),
        }
    ]

# ---------- Header ----------
st.markdown('<div class="main-title">📚 StudyMate AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Your Personal AI Learning Assistant</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="feature-card">💡 <b>Explain</b><br>Pelajari konsep dengan sederhana.</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-card">📝 <b>Summarize</b><br>Dapatkan rangkuman materi.</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="feature-card">❓ <b>Quiz</b><br>Latihan soal interaktif.</div>', unsafe_allow_html=True)

# ---------- Chat history ----------
for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------- Prompt builder ----------
STYLE_INSTRUCTIONS = {
    "Sederhana": (
        "Gunakan Bahasa Indonesia yang sederhana, jelas, dan mudah dipahami mahasiswa. "
        "Jika konsep sulit, gunakan analogi atau contoh."
    ),
    "Santai": (
        "Gunakan Bahasa Indonesia yang santai, ramah, dan natural seperti tutor yang sedang "
        "membantu teman belajar. Tetap akurat dan sopan."
    ),
    "Formal": (
        "Gunakan Bahasa Indonesia yang formal, terstruktur, dan akademis. "
        "Tetap berikan contoh jika membantu pemahaman."
    ),
}

MODE_INSTRUCTIONS = {
    "Penjelasan": (
        "Fokus menjelaskan konsep secara bertahap. Gunakan poin atau contoh bila diperlukan."
    ),
    "Ringkasan": (
        "Fokus memberikan ringkasan yang padat. Utamakan konsep inti, istilah penting, "
        "dan kesimpulan."
    ),
    "Quiz": (
        "Bertindak sebagai tutor quiz. Jika pengguna meminta quiz, buat pertanyaan yang "
        "sesuai topik dan jangan langsung memberikan jawaban kecuali diminta."
    ),
}

SYSTEM_INSTRUCTION = f"""
Kamu adalah StudyMate AI, sebuah AI Learning Assistant untuk membantu mahasiswa belajar.

Tujuan:
- Membantu pengguna memahami materi pembelajaran.
- Memberikan jawaban yang relevan dan terstruktur.
- Jangan mengarang sumber atau fakta. Jika tidak yakin, katakan bahwa kamu tidak yakin.
- Sesuaikan tingkat penjelasan dengan pertanyaan pengguna.
- Untuk pertanyaan akademik, prioritaskan kejelasan dan ketepatan.

Gaya bahasa yang dipilih pengguna:
{STYLE_INSTRUCTIONS[style]}

Mode belajar:
{MODE_INSTRUCTIONS[mode]}
"""

# ---------- User input ----------
prompt = st.chat_input("💬 Tanyakan sesuatu untuk dipelajari...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    if not API_KEY:
        error_message = (
            "⚠️ **GEMINI_API_KEY belum ditemukan.**\n\n"
            "Buat file `.env` berdasarkan `.env.example`, lalu isi API key Gemini kamu."
        )
        with st.chat_message("assistant", avatar="🤖"):
            st.error(error_message)
        st.stop()

    try:
        client = genai.Client(api_key=API_KEY)

        # Convert Streamlit history into Gemini Content objects.
        contents = []
        for message in st.session_state.messages:
            if message["role"] == "user":
                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=message["content"])],
                    )
                )
            elif message["role"] == "assistant":
                contents.append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=message["content"])],
                    )
                )

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("StudyMate sedang berpikir..."):
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=temperature,
                        max_output_tokens=1200,
                    ),
                )

                answer = response.text or "Maaf, saya belum mendapatkan respons."
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as exc:
        with st.chat_message("assistant", avatar="🤖"):
            st.error(
                "Terjadi error saat menghubungi Gemini. "
                "Periksa API key, koneksi internet, dan nama model."
            )
            with st.expander("Detail error"):
                st.code(str(exc))
