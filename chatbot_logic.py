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
        # Define the list of models to try in order of preference
        # Moving away from gemini-2.0-flash due to quota limits
        models_to_try = [
            "gemini-flash-latest",
            "gemini-pro-latest",
            "gemini-2.0-flash-lite-preview-02-05",
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash"
        ]

        response = None
        last_exception = None

        for model_name in models_to_try:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.7))
                if response:
                    print(f"Successfully generated with {model_name}")
                    break
            except Exception as e:
                print(f"Failed with {model_name}: {e}")
                last_exception = e
                continue
        
        if not response and last_exception:
            raise last_exception

        questions = response.text.strip().split('\n')
        # Filter out empty strings and potential markdown list indicators if any, then strip whitespace
        filtered_questions = [q.strip().lstrip('*- ').strip() for q in questions if q.strip()]

        # Ensure we return 3 to 5 questions
        if len(filtered_questions) < 3:
            # Fallback if LLM doesn't generate enough
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
        error_details = str(e)
        return [f"Error: Could not generate questions. (Details: {e})"]

def handle_fallback():
    """Provides a fallback response for unclear input."""
    return "I'm sorry, I didn't quite catch that. Could you please rephrase or tell me how I can assist you? 🤔"

def end_conversation():
    """Gracefully concludes the conversation with a positive closing."""
    return "Thank you for your time and for sharing your information! Your details and answers have been successfully recorded. We'll be in touch very soon regarding the next steps in our hiring process. Have a fantastic day! 😊👋"

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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