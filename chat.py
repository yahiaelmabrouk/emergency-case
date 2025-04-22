from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

app = Flask(__name__)

model_name = "tiiuae/falcon-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

chatbot_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=200)

@app.route('/')
def home():
    return jsonify({"message": "Emergency Chatbot with Falcon-7B-Instruct is running!"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        prompt = f"You are an emergency chatbot specializing in medical cases. Respond to the following question with clear and actionable instructions:\n{user_input}"
        response = chatbot_pipeline(prompt, max_length=200, num_return_sequences=1)
        chatbot_reply = response[0]["generated_text"]
        return jsonify({"response": chatbot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)