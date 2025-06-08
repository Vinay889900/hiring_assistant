# 🤖 AI-Powered Hiring Assistant Chatbot

An intelligent chatbot built with **Streamlit** and **Gemini API** to automate the initial screening process of candidates in a tech recruitment setting. It collects candidate information and generates personalized technical questions based on the declared tech stack.

---

## 📌 Project Overview

The **Hiring Assistant Chatbot** assists a fictional recruitment agency, **TalentScout**, by:
- Collecting candidate information through a conversational UI.
- Dynamically generating technical questions based on the candidate's provided tech stack.
- Ensuring a coherent and seamless user experience using LLMs.

---

## 🧰 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM Integration**: Gemini API (Google Generative AI)
- **Environment**: `.env` for API key management
- **Deployment**: Render
---

## ⚙️ Installation Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/hiring-assistant-chatbot.git
cd hiring-assistant-chatbot

2. Install Dependencies

Create a virtual environment (recommended) and install dependencies:

pip install -r requirements.txt

3. Set Up Environment Variables

Create a .env file in the root directory:

GEMINI_API_KEY=your_actual_api_key_here

4. Run the App

streamlit run app.py


---

🚀 Usage Guide

1. Launch the Streamlit app.


2. Enter candidate details when prompted (name, email, experience, tech stack, etc.).


3. The chatbot will generate and display relevant technical questions.


4. The session ends with a professional closing message.




---

🧠 Features

Friendly conversational interface

Collects and validates candidate data

Generates tech-stack-specific questions

Handles context and fallback gracefully

Designed using prompt engineering best practices


---

🧪 Prompt Design

Prompts were carefully engineered to:

Collect structured candidate details

Generate 3–5 relevant questions per tech skill

Handle diverse tech stacks like Python, Django, React, SQL, etc.

Maintain a smooth and human-like conversation flow



---

✅ Example Tech Stack & Output

Input:

Tech Stack: Python, Django, MySQL

Generated Questions:

How does Django’s ORM work with relational databases?

What is the difference between a list and a tuple in Python?

How do you manage database migrations in Django?



---

🔒 Data Privacy

No real data is stored.

API key is stored securely using .env.

Designed with simulated or anonymized input data.



---

🛠 Future Enhancements

Sentiment analysis to assess candidate emotions

Multilingual support

Admin panel for recruiters to review responses


