# 🥗 Personalized Diet Plan Generator Using Groq LLM

A user-friendly Streamlit application that generates a **custom diet plan** tailored to your personal information, health goals, food preferences, allergies, and more — all powered by **Groq LLM** through LangChain.

---

## 🚀 Features

- 🔒 Secure input handling with environment variables
- 🤖 AI-generated diet plan using LLMChain from LangChain
- 📅 Day-by-day meal breakdown including snacks & hydration
- 🛒 Weekly shopping list for meal prep
- 📥 Downloadable plan in **Text** and **PDF** format
- 🌐 Fully interactive UI built with Streamlit

---



---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**
- **LangChain**
- **Groq LLM**
- **FPDF** (for PDF generation)
- **dotenv** (for secure API keys)

---

## 🧠 How It Works

1. The user fills out a form with their details (e.g., weight, height, goals, restrictions).
2. Inputs are passed into a LangChain `LLMChain` that uses Groq's LLaMA-4 model.
3. The AI returns a structured plan formatted by a prompt template.
4. The plan is displayed in the app and can be downloaded as a `.txt` or `.pdf` file.

---


