🤖 AI-Powered Hiring Assistant Chatbot

An intelligent chatbot built with Streamlit and Gemini API to automate the initial screening process of candidates in a tech recruitment setting. It collects candidate information and generates personalized technical questions based on the declared tech stack.


---

📌 Project Overview

The Hiring Assistant Chatbot assists a fictional recruitment agency, TalentScout, by:

Collecting candidate information through a conversational UI

Dynamically generating technical questions based on the candidate's provided tech stack

Ensuring a coherent and seamless user experience using LLMs



---

🧰 Tech Stack

Frontend: Streamlit

Backend: Python

LLM Integration: Gemini API (Google Generative AI)

Environment: .env for API key management

Deployment: Render



---

⚙️ Installation Instructions

1. Clone the Repository

git clone https://github.com/your-username/hiring-assistant-chatbot.git
cd hiring-assistant-chatbot

2. Install Dependencies

It's recommended to use a virtual environment:

pip install -r requirements.txt

3. Set Up Environment Variables

Create a .env file in the root directory and add your Gemini API key:

GEMINI_API_KEY=your_actual_api_key_here

4. Run the App

streamlit run app.py


---

🚀 Usage Guide

Start the Streamlit app

Enter candidate details (name, email, experience, tech stack, etc.)

The chatbot will generate and display relevant technical questions

Ends with a thank-you and next steps



---

🧠 Features

Friendly conversational UI

Collects and validates candidate info

Generates relevant questions based on tech stack

Maintains conversation flow with context

Graceful fallback for unexpected inputs



---

🧪 Prompt Design Strategy

Prompts are designed to:

Collect structured candidate information

Generate 3–5 questions per listed skill

Adapt to diverse tech stacks (e.g., Python, React, Django)

Maintain a natural and coherent conversation



---

✅ Example Input & Output

Input:
Tech Stack: Python, Django, MySQL

Output:

How does Django’s ORM work with relational databases?

What is the difference between a list and a tuple in Python?

How do you manage database migrations in Django?



---

🔐 Data Privacy

No real user data is stored

.env used to securely manage API keys

Uses simulated or anonymized test data



---

🛠️ Future Enhancements

Sentiment analysis for emotion tracking

Multilingual support

Recruiter admin panel for reviewing submissions



---
