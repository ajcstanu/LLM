from flask import Flask, request, jsonify
import fitz  # For PDF processing
from ollama import Ollama
import nltk
from nltk.corpus import stopwords  # Example for text preprocessing
nltk.download('punkt')  # Download necessary NLTK data
nltk.download('stopwords')
def preprocess_text(text):
    """Preprocess text by tokenizing and removing stop words"""
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens
def answer_question(text, question):
    """
    Uses Ollama LLM to answer questions based on the given text.
    """
    ollama = Ollama(model="llama2")
    prompt = f"Context: {text}\n\nQuestion: {question}\n\nAnswer:"
    response = ollama(prompt)
    return response
app = Flask(__name__)
@app.route("/upload_document", methods=["POST"])
def upload_and_answer():
    try:
        data = request.json
        file_path = data.get("file_path")
        question = data.get("question")

        if not file_path or not question:
            return jsonify({"error": "Missing file_path or question"}), 400
        # Read PDF content
        with fitz.open(file_path) as doc:
            text = " ".join([page.get_text() for page in doc])
        preprocessed_text = " ".join(preprocess_text(text))
        answer = answer_question(preprocessed_text, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle exceptions

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8502)
