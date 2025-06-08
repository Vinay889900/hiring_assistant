import os
import google.generativeai as genai

def greet_candidate():
    """Greets the candidate and explains the chatbot's purpose with emojis."""
    return "👋 Hello there! I'm your **TalentScout AI Assistant**. I'm here to gather some quick information and then ask a few technical questions based on your skills. Let's make this quick and smooth! ✨"

def generate_technical_questions(tech_stack):
    """Generates technical questions based on the provided tech stack using Gemini LLM."""
    if not tech_stack:
        return ["🤔 It looks like you haven't provided your tech stack yet. Please tell me your key skills so I can generate relevant questions!"]

    # Construct a clear and concise prompt for Gemini
    prompt = (
        f"Generate 3 to 5 highly relevant and concise technical interview questions for a candidate "
        f"who is skilled in: {', '.join(tech_stack)}. "
        f"Format the output as a simple numbered list, with no introductory or concluding sentences, "
        f"just the questions themselves. Ensure questions are diverse if multiple topics are provided."
    )

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash") # Using gemini-1.5-flash for speed and cost-efficiency
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.7))

        questions = response.text.strip().split('\n')
        # Filter out empty strings and potential markdown list indicators if any, then strip whitespace
        filtered_questions = [q.strip().lstrip('*- ').strip() for q in questions if q.strip()]

        # Ensure we return 3 to 5 questions, even if the LLM sometimes gives more/less
        if len(filtered_questions) < 3:
            # Fallback if LLM doesn't generate enough, or generate more general questions
            print("Warning: LLM generated fewer than 3 questions. Appending general ones.")
            general_fallback_questions = [
                f"Describe a challenging technical problem you've solved using one of your listed skills ({tech_stack[0]} perhaps?).",
                "How do you stay updated with the latest trends and technologies in your field?",
                "What's your approach to debugging complex issues?"
            ]
            for q in general_fallback_questions:
                if q not in filtered_questions:
                    filtered_questions.append(q)

        return filtered_questions[:5] # Ensure max of 5 questions

    except Exception as e:
        print(f"❌ Error generating questions from Gemini: {e}")
        # Return a user-friendly error message
        return [f"Error: I encountered an issue generating technical questions at this moment due to an API error. Please ensure your Gemini API key is correctly set and try again. (Details: {e})"]

def handle_fallback():
    """Provides a fallback response for unclear input."""
    return "I'm sorry, I didn't quite catch that. Could you please rephrase or tell me how I can assist you? 🤔"

def end_conversation():
    """Gracefully concludes the conversation with a positive closing."""
    return "Thank you for your time and for sharing your information! Your details and answers have been successfully recorded. We'll be in touch very soon regarding the next steps in our hiring process. Have a fantastic day! 😊👋"

if __name__ == "__main__":
    # Example usage for testing functions directly
    print(greet_candidate())
    print("\n--- Example 1: Python & React ---")
    tech_stack_example_1 = ["Python", "React"]
    questions_1 = generate_technical_questions(tech_stack_example_1)
    for q in questions_1:
        print(f"- {q}")

    print("\n--- Example 2: AWS & SQL ---")
    tech_stack_example_2 = ["AWS", "SQL"]
    questions_2 = generate_technical_questions(tech_stack_example_2)
    for q in questions_2:
        print(f"- {q}")

    print("\n" + end_conversation())