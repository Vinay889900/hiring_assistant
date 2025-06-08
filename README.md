🤖 AI-Powered Hiring Assistant Chatbot

A conversational AI chatbot that helps streamline the tech hiring process by collecting candidate details and dynamically generating relevant technical questions based on the candidate's tech stack.


---

🚀 Features

🗣️ Conversational UI with Streamlit

📋 Candidate Information Collection

🔍 Tech-Stack Specific Question Generation

🧠 Powered by Gemini API (Google Generative AI)

🔐 Secure API Key Handling with .env

☁️ Deployed on Render (or local via Streamlit)



---

🛠️ Tech Stack

Python

Streamlit

Gemini API

dotenv (.env for secure config)



---

🧩 How It Works

1. User launches the chatbot interface.


2. Chatbot collects candidate data (name, email, experience, tech stack).


3. Tech stack parsed, and a prompt is sent to Gemini API.


4. API returns custom technical questions for the provided stack.


5. Chatbot displays the questions and thanks the user.




---

⚙️ Installation

# Clone the repository
git clone https://github.com/your-username/hiring-assistant-chatbot.git
cd hiring-assistant-chatbot

# Install dependencies
pip install -r requirements.txt


---

🔐 API Key

Create a .env file in the root folder and add:

GEMINI_API_KEY=your_actual_api_key_here


---

▶️ Running the App

streamlit run app.py


---

💡 Example Use Case

Tech Stack Input: Python, Django, MySQL
Generated Questions:

How does Django’s ORM work with relational databases?

What is the difference between a list and a tuple in Python?

How do you manage database migrations in Django?



---

🛡️ Data Privacy

No personal data stored

API key securely managed with .env

Safe for testing and academic demos



---

🛠️ Future Enhancements

Sentiment analysis

Multilingual candidate support

Admin dashboard for recruiter review



---
