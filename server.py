from flask import Flask, request
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

@app.route("/chat", methods=["GET"])
def chatbot():
    user_input = request.args.get("message", "")
    doc = nlp(user_input)
    response = f"You said: {user_input}. Detected {len(doc)} words."
    return {"response": response}

if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=environ.get("PORT", 5000))
