# 🥗 Personalized Diet Plan Generator

A customizable web app built using **Streamlit**, **Python**, **LangChain**, and **Groq’s LLM**, designed to generate detailed and downloadable diet plans tailored to your personal health information, preferences, and goals.

---

## 🌟 Features

- Collects personal details like age, weight, activity level, health conditions, etc.
- Uses **Groq's powerful LLM** to generate diet plans day-by-day for 1–4 weeks
- Includes:
  - Meal timing & simple recipe ideas
  - Daily hydration tips
  - Snack suggestions
  - PDF and Text download options
- Automatically generates a shopping list for the first week
- Fully responsive Streamlit UI

---
## 📂 Project Structure

Diet-Plan-Generator/
│

├── DietPlanner/
│ ├── main.py # Main Streamlit app
│ └── .env # (Hidden) file for API key
│

├── requirements.txt # All dependencies
└── README.md # This file



---

## 🧪 Getting Started

### 🔧 Prerequisites

- Python 3.9+
- A Groq API Key

---

### 📦 Installation

# 1. Clone the repo
git clone https://github.com/yourusername/diet-plan-generator.git
cd diet-plan-generator/DietPlanner

# 2. Install dependencies
pip install -r ../requirements.txt

# 3. Set up environment variable
echo GROQ_API_KEY=your_groq_api_key > .env

# 4. Run the app
streamlit run main.py


###📝 Environment Variable

Create a .env file in the root folder (DietPlanner/) with:
GROQ_API_KEY=your_actual_groq_api_key

📥 Output Formats:

📝 Downloadable .txt plan
📄 Printable .pdf plan
✅ Includes shopping list and success tips.

📋 Summary:

This project is a user-friendly web app that generates personalized diet plans based on your inputs like age, health goals, dietary preferences, and more. Built with Python, Streamlit, and integrated with Groq’s LLM via LangChain, it creates detailed daily meal plans and allows you to download them in Text or PDF format. Ideal for anyone looking to start or maintain a healthy eating routine with AI-powered customization.
