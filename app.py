from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Set the API key directly (Replace with your actual API key)
client = Groq(api_key="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")

# Function to call the API and get gift suggestions
def get_gift_suggestions(user_data):
    user_message = (f"I am looking for a gift for a {user_data['occasion']}. "
                    f"It's for my {user_data['recipient']}, who is {user_data['age']} years old. "
                    f"They are interested in {user_data['interest']}. "
                    f"Here's a description: {user_data['description']}. "
                    f"My budget is {user_data['budget']} rupees. "
                    f"The gift should be rated based on: "
                    f"Uniqueness: {user_data['uniqueness']}, "
                    f"Personalized: {user_data['personalized']}, "
                    f"Price importance: {user_data['price_importance']}, "
                    f"Practicality vs Aesthetics: {user_data['practicality_vs_aesthetics']}, "
                    f"Emotional value: {user_data['emotional_value']}, "
                    f"Hobby importance: {user_data['hobby_importance']}, "
                    f"Surprise appreciation: {user_data['surprise_appreciation']}, "
                    f"Lasting impact: {user_data['lasting_impact']}, "
                    f"Packaging importance: {user_data['packaging_importance']}, "
                    f"Daily use: {user_data['daily_use']}.")

    # Call the API for gift suggestions
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ("You are a helpful gifting assistant. Use the information provided "
                            "to suggest personalized gifts. Consider the occasion, recipient, interests, "
                            "budget, ratings, and description.")
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        model="llama3-8b-8192",  # Replace with the appropriate model for your use case
    )

    return chat_completion.choices[0].message.content

# Function to ask additional questions and refine suggestions
def ask_additional_questions(user_data, additional_info):
    # Use Groq's chat completion API to ask additional questions dynamically
    follow_up_question = ""
    user_message = (f"I'm looking for a gift for a {user_data['occasion']}. The recipient is "
                    f"{user_data['age']} years old, and they enjoy {user_data['interest']}. "
                    f"My budget is {user_data['budget']}.")

    if additional_info:
        user_message += f" Here's more information: {additional_info}."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant helping someone choose a personalized gift. Ask questions to better understand their preferences."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        model="llama3-8b-8192"
    )

    # Return the follow-up question
    follow_up_question = chat_completion.choices[0].message.content
    return follow_up_question

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    user_data = request.json
    suggestions = get_gift_suggestions(user_data)
    return jsonify({'suggestions': suggestions})

@app.route('/ask_questions', methods=['POST'])
def ask_questions():
    user_data = request.json['user_data']
    additional_info = request.json.get('additional_info', '')
    follow_up_question = ask_additional_questions(user_data, additional_info)
    return jsonify({'question': follow_up_question})

if __name__ == '__main__':
    app.run(debug=True)
