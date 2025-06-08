import streamlit as st
import os
import json
# Import your functions from chatbot_logic. No need for dotenv here directly.
from chatbot_logic import greet_candidate, generate_technical_questions, end_conversation
import google.generativeai as genai
from dotenv import load_dotenv # <--- Import load_dotenv here!

# Load environment variables from .env file FIRST THING in this module
load_dotenv()

# Configure the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Check if the API key was successfully loaded
if not GEMINI_API_KEY:
    # This warning will now appear if the .env file is missing/incorrect
    # or if GEMINI_API_KEY isn't set in the environment.
    print("⚠️ GEMINI_API_KEY environment variable not found. Please ensure it's set in your .env file or system environment.")
    # For a robust application, you might want to raise an exception here
    # or provide a more graceful exit. For now, we'll assign a placeholder
    # which will cause the API calls to fail but prevent the script from crashing immediately.
    # In a deployed app, you'd want a hard stop if the key isn't present.
    raise ValueError("GEMINI_API_KEY is not set. Please set it in your .env file.")


genai.configure(api_key=GEMINI_API_KEY)




# ---------------- Page Config -------------------
st.set_page_config(page_title="TalentScout AI Interviewer 🌟", page_icon="🤖", layout="centered")

# ---------------- Custom CSS Styling -------------------
st.markdown("""
<style>
    /* Overall App Styling */
    .stApp {
        background: linear-gradient(to bottom right, #e0f7fa, #ffffff); /* Gentle gradient background */
        color: #333333; /* Darker text for contrast */
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Header Styling */
    h1 {
        color: #1a237e; /* Deep blue for header */
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.7rem;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.15);
        padding-top: 15px;
    }

    /* Chat Message Styling */
    .stChatMessage {
        border-radius: 25px; /* More rounded, softer look */
        padding: 18px 22px;
        margin-bottom: 15px;
        font-size: 1.08rem;
        line-height: 1.65;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); /* More prominent shadow */
        transition: transform 0.2s ease-out, box-shadow 0.2s ease-out; /* Smooth transition */
        animation: fadeIn 0.5s ease-out; /* Fade in animation */
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* User Message Styling */
    .stChatMessage.stChatMessage-user {
        background-color: #bbdefb; /* Lighter blue, more friendly */
        border-left: 7px solid #2196f3; /* Stronger blue accent */
        text-align: left;
        margin-left: 20%; /* Pushes user messages to the right */
        border-bottom-left-radius: 5px; /* Square off bottom-left for user */
    }

    /* Assistant Message Styling */
    .stChatMessage.stChatMessage-assistant {
        background-color: #dcedc8; /* Soft green, calming */
        border-left: 7px solid #4caf50; /* Stronger green accent */
        text-align: left;
        margin-right: 20%; /* Pushes assistant messages to the left */
        border-bottom-right-radius: 5px; /* Square off bottom-right for assistant */
    }

    /* Chat Input Container */
    .stChatInputContainer {
        margin-top: 40px;
        padding: 25px;
        border-top: 1px solid #e0e0e0;
        background-color: #ffffff; /* White background */
        border-radius: 20px; /* More rounded */
        box-shadow: 0 -5px 20px rgba(0,0,0,0.08); /* Stronger shadow for "floating" effect */
        position: sticky; /* Keeps it at the bottom */
        bottom: 0;
        z-index: 1000;
        margin-left: -1rem; /* Adjust for padding on small screens */
        margin-right: -1rem;
        width: calc(100% + 2rem); /* Ensure full width */
    }
    .stChatInputContainer > div > div > label {
        font-size: 1.1rem; /* Larger label for input */
        font-weight: 600;
        color: #555555;
    }

    /* Streamlit Button Styling */
    .stButton > button {
        background-color: #673ab7; /* Deep purple */
        color: white;
        border-radius: 12px; /* More rounded buttons */
        padding: 0.9rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.25); /* More prominent shadow */
        transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
        letter-spacing: 0.5px;
    }
    .stButton > button:hover {
        background-color: #512da8; /* Darker purple on hover */
        transform: translateY(-4px); /* Lift effect */
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Primary button for "Start New Conversation" / "Submit" */
    /* Targeting by data-testid or specific class if type="primary" is used */
    .stButton[data-testid*="primary"] > button,
    .stButton.css-1r6dm7b > button { /* Specific class for primary if present */
        background-color: #007bff; /* Bright blue for primary actions */
        box-shadow: 0 5px 15px rgba(0,123,255,0.3);
    }
    .stButton[data-testid*="primary"] > button:hover,
    .stButton.css-1r6dm7b > button:hover {
        background-color: #0056b3;
        box-shadow: 0 8px 20px rgba(0,123,255,0.4);
    }

    /* Text Area Styling for detailed inputs (Tech Stack, Answers) */
    .stTextArea > label {
        font-weight: 600;
        color: #495057;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }
    .stTextArea > div > div > textarea {
        border-radius: 15px; /* More rounded */
        border: 1px solid #ced4da;
        padding: 15px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.08); /* Subtle inset shadow */
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        font-size: 1rem;
        min-height: 120px; /* Ensure sufficient height */
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 0.25rem rgba(0,123,255,.25); /* Focus ring */
        outline: none;
    }

    /* Alerts (Info, Success, Warning, Error) */
    .stAlert {
        border-radius: 15px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        font-size: 1.05rem;
        line-height: 1.5;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .stAlert.stAlert-info { background-color: #e3f2fd; border-left: 6px solid #2196f3; }
    .stAlert.stAlert-success { background-color: #e8f5e9; border-left: 6px solid #4caf50; }
    .stAlert.stAlert-warning { background-color: #fff3e0; border-left: 6px solid #ff9800; }
    .stAlert.stAlert-error { background-color: #ffebee; border-left: 6px solid #f44336; }

    /* Footer / Bottom Section */
    .bottom-section {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- State Initialization -------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'greeting'
if 'candidate_info' not in st.session_state:
    st.session_state.candidate_info = {
        'full_name': '', 'email': '', 'phone': '',
        'experience': '', 'position': '',
        'location': '', 'tech_stack': []
    }
if 'tech_questions' not in st.session_state:
    st.session_state.tech_questions = []
if 'conversation_ended' not in st.session_state:
    st.session_state.conversation_ended = False
if 'Youtubes' not in st.session_state: # Renamed from 'Youtubes' for clarity
    st.session_state.Youtubes = {}

# ---------------- Utility Functions -------------------
def save_candidate_data():
    """Saves candidate data to a JSON file."""
    data_dir = "candidate_data"
    os.makedirs(data_dir, exist_ok=True)

    candidate_name = st.session_state.candidate_info.get('full_name', 'unknown_candidate').replace(' ', '_').replace('/', '').replace('\\', '')
    candidate_email_prefix = st.session_state.candidate_info.get('email', 'noemail').split('@')[0]
    filename = f"{data_dir}/{candidate_name}_{candidate_email_prefix}.json"

    try:
        with open(filename, 'w') as f:
            json.dump({
                'candidate_info': st.session_state.candidate_info,
                'technical_questions': st.session_state.tech_questions,
                'technical_answers': st.session_state.Youtubes, # Using 'Youtubes'
                'conversation_history': st.session_state.messages
            }, f, indent=4)
        st.success(f"✅ Your data has been successfully saved as `{filename}`!")
    except Exception as e:
        st.error(f"⚠️ Oh no! There was an error saving your data: {e}")

def reset_conversation():
    """Resets all session state variables to start a new conversation."""
    st.session_state.messages = []
    st.session_state.current_step = 'greeting'
    st.session_state.candidate_info = {
        'full_name': '', 'email': '', 'phone': '',
        'experience': '', 'position': '',
        'location': '', 'tech_stack': []
    }
    st.session_state.tech_questions = []
    st.session_state.conversation_ended = False
    st.session_state.Youtubes = {} # Using 'Youtubes'
    st.rerun()

# ---------------- Header -------------------
st.title("TalentScout AI Interviewer 🌟")
st.markdown("---")

# ---------------- Message Display Area -------------------
# Display chat messages from history on app rerun
chat_placeholder = st.container() # Create a container for messages
with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ---------------- Main Conversation Logic -------------------
# Use a single chat input at the bottom, dynamic based on step
user_input_key = "chat_input_general"
current_step = st.session_state.current_step

if st.session_state.conversation_ended:
    st.info("🎉 **Conversation Completed!** Thank you for your time with TalentScout. We'll be in touch soon!")
    if st.button("Start New Conversation 🔄", type="primary"):
        reset_conversation()
else:
    # --- Initial Greeting and Info Collection ---
    if current_step == 'greeting':
        if not st.session_state.messages:
            greeting_msg = greet_candidate()
            with st.chat_message("assistant"):
                st.markdown(greeting_msg)
            st.session_state.messages.append({"role": "assistant", "content": greeting_msg})
            st.session_state.current_step = 'ask_name'
            st.rerun() # Rerun to display the greeting

    elif current_step == 'ask_name':
        prompt_text = "👤 What's your full name?"
        if user_response := st.chat_input(prompt_text, key=user_input_key):
            if len(user_response.strip()) > 1:
                with st.chat_message("user"):
                    st.markdown(user_response)
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.candidate_info['full_name'] = user_response.strip()
                ai_response = f"Nice to meet you, **{user_response.strip()}**! 👋"
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.current_step = 'ask_email'
                st.rerun()
            else:
                st.toast("Please enter a valid full name. 🤔", icon="⚠️")

    elif current_step == 'ask_email':
        prompt_text = "📧 Could you please share your email address?"
        if user_response := st.chat_input(prompt_text, key=user_input_key):
            if '@' in user_response and '.' in user_response:
                with st.chat_message("user"):
                    st.markdown(user_response)
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.candidate_info['email'] = user_response.strip()
                ai_response = "Got it! Your email has been recorded. 📧"
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.current_step = 'ask_phone'
                st.rerun()
            else:
                st.toast("Please enter a valid email address. ❌", icon="⚠️")

    elif current_step == 'ask_phone':
        prompt_text = "📞 What's your phone number?"
        if user_response := st.chat_input(prompt_text, key=user_input_key):
            if len(user_response.strip()) >= 8 and user_response.strip().replace(' ', '').replace('-', '').isdigit():
                with st.chat_message("user"):
                    st.markdown(user_response)
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.candidate_info['phone'] = user_response.strip()
                ai_response = "Thanks for your phone number! 📞"
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.current_step = 'ask_experience'
                st.rerun()
            else:
                st.toast("Please enter a valid phone number (at least 8 digits, numbers only). 🔢", icon="⚠️")

    elif current_step == 'ask_experience':
        prompt_text = "💼 How many years of professional experience do you have? (e.g., 5)"
        if user_response := st.chat_input(prompt_text, key=user_input_key):
            if user_response.strip().isdigit():
                with st.chat_message("user"):
                    st.markdown(user_response)
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.candidate_info['experience'] = user_response.strip()
                ai_response = f"Okay, **{user_response.strip()} years** of experience. That's helpful! 👍"
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.current_step = 'ask_position'
                st.rerun()
            else:
                st.toast("Please enter a number for years of experience. 🧐", icon="⚠️")

    elif current_step == 'ask_position':
        prompt_text = "🎯 What kind of position(s) are you interested in? (e.g., Software Engineer, Data Scientist)"
        if user_response := st.chat_input(prompt_text, key=user_input_key):
            if len(user_response.strip()) > 2:
                with st.chat_message("user"):
                    st.markdown(user_response)
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.candidate_info['position'] = user_response.strip()
                ai_response = f"Understood, you're interested in **{user_response.strip()}** roles. 🚀"
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.current_step = 'ask_location'
                st.rerun()
            else:
                st.toast("Please tell me about the positions you're interested in. 📝", icon="⚠️")

    elif current_step == 'ask_location':
        prompt_text = "🌍 What's your current or preferred work location? (e.g., Bengaluru, Remote)"
        if user_response := st.chat_input(prompt_text, key=user_input_key):
            if len(user_response.strip()) > 2:
                with st.chat_message("user"):
                    st.markdown(user_response)
                st.session_state.messages.append({"role": "user", "content": user_response})
                st.session_state.candidate_info['location'] = user_response.strip()
                ai_response = f"Great! Your location is **{user_response.strip()}**. 📍 Now, let's talk tech!"
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.current_step = 'ask_tech_stack'
                st.rerun()
            else:
                st.toast("Please provide your location. 🌎", icon="⚠️")

    # --- Tech Stack Input (multi-line) ---
    elif current_step == 'ask_tech_stack':
        # Prompt for tech stack will be directly in the chat message
        if not st.session_state.messages[-1]["content"].startswith("🛠️ Tell me about your primary tech stack"): # Avoid repeating prompt
             tech_stack_prompt = "🛠️ Tell me about your primary tech stack or key skills, separated by commas (e.g., Python, React, AWS, SQL). This helps me tailor questions for you!"
             with st.chat_message("assistant"):
                 st.markdown(tech_stack_prompt)
             st.session_state.messages.append({"role": "assistant", "content": tech_stack_prompt})

        # Use a text area for tech stack input, displayed explicitly
        st.markdown("<div style='margin-top: 20px; padding: 15px; border-radius: 10px; background-color: #f0f0f0;'>", unsafe_allow_html=True)
        tech_stack_input = st.text_area("Your Tech Stack", key="tech_input_area", height=120, placeholder="Example: Python, Django, React, Kubernetes")
        if st.button("Submit Tech Stack ✅", key="submit_tech_stack_btn", type="primary"):
            if tech_stack_input.strip():
                techs = [t.strip() for t in tech_stack_input.split(',') if t.strip()]
                st.session_state.candidate_info['tech_stack'] = techs
                user_msg = f"My tech stack includes: {', '.join(techs)}"
                with st.chat_message("user"):
                    st.markdown(user_msg)
                st.session_state.messages.append({"role": "user", "content": user_msg})

                with st.spinner("✨ Generating tailored technical questions... This might take a moment!"):
                    questions = generate_technical_questions(techs)
                    if questions and "Error:" not in questions[0]:
                        st.session_state.tech_questions = questions
                        question_msg = "Excellent! Here are a few technical questions for you. Please answer them in detail. Take your time! 👇"
                        for idx, q in enumerate(questions, 1):
                            question_msg += f"\n\n**Q{idx}.** {q}"
                        with st.chat_message("assistant"):
                            st.markdown(question_msg)
                        st.session_state.messages.append({"role": "assistant", "content": question_msg})
                        st.session_state.Youtubes = {f"Q{i}": "" for i in range(1, len(questions) + 1)} # Using 'Youtubes'
                        st.session_state.current_step = 'technical_questions'
                        st.rerun()
                    else:
                        error_msg = f"⚠️ I encountered an issue generating questions for your tech stack. Please try again or simplify your tech stack. {questions[0]}"
                        with st.chat_message("assistant"):
                            st.markdown(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                st.toast("Please list your tech stack before submitting. 🤔", icon="⚠️")
        st.markdown("</div>", unsafe_allow_html=True)


    # --- Technical Questions & Answers ---
    elif current_step == 'technical_questions':
        # Display questions and text areas dynamically
        st.markdown("### 📝 Your Technical Answers:", unsafe_allow_html=True)
        st.info("💡 Please provide detailed answers for each question below. You can edit them before submitting.")

        with st.form("technical_answers_form", clear_on_submit=False):
            for idx, q in enumerate(st.session_state.tech_questions, 1):
                default_answer = st.session_state.Youtubes.get(f"Q{idx}", "") # Using 'Youtubes'
                answer = st.text_area(f"**Question {idx}:** {q}", key=f"ans_{idx}", value=default_answer, height=180)
                st.session_state.Youtubes[f"Q{idx}"] = answer # Update state as user types # Using 'Youtubes'

            submitted = st.form_submit_button("Submit All Answers ✨", type="primary")
            if submitted:
                if all(st.session_state.Youtubes[q_key].strip() for q_key in st.session_state.Youtubes): # Using 'Youtubes'
                    final_user_response = "Here are my answers to the technical questions: \n\n"
                    for idx, q in enumerate(st.session_state.tech_questions, 1):
                        answer = st.session_state.Youtubes[f"Q{idx}"] # Using 'Youtubes'
                        final_user_response += f"**Q{idx}:** {q}\n**A:** {answer}\n\n"

                    with st.chat_message("user"):
                        st.markdown(final_user_response)
                    st.session_state.messages.append({"role": "user", "content": final_user_response})

                    end_msg = end_conversation()
                    with st.chat_message("assistant"):
                        st.markdown(end_msg)
                    st.session_state.messages.append({"role": "assistant", "content": end_msg})
                    st.session_state.conversation_ended = True
                    save_candidate_data()
                    st.rerun()
                else:
                    st.toast("Please answer all the technical questions before submitting. 🙏", icon="⚠️")

    # --- End Conversation Button (always visible unless conversation completed or at greeting) ---
    if not st.session_state.conversation_ended and current_step != 'greeting':
        st.markdown("---")
        st.markdown("<div class='bottom-section'>", unsafe_allow_html=True)
        if st.button("End Conversation Early 👋", help="Click here to end the conversation and save your progress so far."):
            end_msg = end_conversation()
            with st.chat_message("assistant"):
                st.markdown(end_msg)
            st.session_state.messages.append({"role": "assistant", "content": end_msg})
            st.session_state.conversation_ended = True
            save_candidate_data()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)