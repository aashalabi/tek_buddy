import os
from dotenv import load_dotenv

load_dotenv()  # Load .env only in development


import uuid

from flask import Flask, request, jsonify

from rag import rag, client,llm, get_answer

import db
import json
app = Flask(__name__)
PORT = int(os.getenv("APP_PORT", 5000))


@app.route('/')
def greetings():
    return 'Welcome to Tek Buddy'

@app.route("/question", methods=["GET", "POST"])
def handle_question():
    data = request.json
    print('data')
    print(data)
    question = data["question"]

    if not question:
        return jsonify({"error": "No question provided"}), 400

    conversation_id = str(uuid.uuid4())

    answer_data = get_answer(question, model_choice='openai/gpt-3.5-turbo')
    print('answer_data')
    print(answer_data)

    result = {
        "conversation_id": conversation_id,
        "question": question,
        "answer": answer_data,# ["answer"],
    }
    
    db.save_conversation(
        conversation_id=conversation_id,
        question=question,
        answer_data=answer_data,
    )
    

    return jsonify(result)

@app.route("/feedback", methods=["POST"])
def handle_feedback():
    data = request.json
    conversation_id = data["conversation_id"]
    feedback = data["feedback"]

    if not conversation_id or feedback not in [1, -1]:
        return jsonify({"error": "Invalid input"}), 400
    
    db.save_feedback(
        conversation_id=conversation_id,
        feedback=feedback,
    )
    
    result = {
        "message": f"Feedback received for conversation {conversation_id}: {feedback}"
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)