from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Initialize Flask app
app = Flask(__name__)

# Load Falcon-7B-Instruct model and tokenizer
model_name = "tiiuae/falcon-7b-instruct"  # Falcon-7B-Instruct from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# Initialize a pipeline for text generation
chatbot_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=200)

# Home route to check if the app is running
@app.route('/')
def home():
    return jsonify({"message": "Emergency Chatbot with Falcon-7B-Instruct is running!"})

# Route to handle chatbot responses
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user input from the request
        user_input = request.json.get('message', '')
        
        # Ensure input is not empty
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Create a prompt for the chatbot to generate a response
        prompt = f"You are an emergency chatbot specializing in medical cases. Respond to the following question with clear and actionable instructions:\n{user_input}"
        
        # Generate a response using Falcon-7B-Instruct
        response = chatbot_pipeline(prompt, max_length=200, num_return_sequences=1)
        
        # Extract the generated text
        chatbot_reply = response[0]["generated_text"]
        
        # Return the response
        return jsonify({"response": chatbot_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)