from flask import Flask, render_template, request, redirect, url_for, session, flash
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Global variables for AI model
primary_model_path = "ibm-granite/granite-3.0-3b-a800m-instruct"
fallback_model_path = "microsoft/DialoGPT-small"  # lightweight model for CPU testing
tokenizer = None
model = None
device = None

# In-memory storage (replace with database in production)
chat_history = []
sentiment_data = {'positive': 0, 'neutral': 0, 'negative': 0}
concerns = []

def initialize_model():
    """Initialize the IBM Granite model, with fallback to a smaller model"""
    global tokenizer, model, device

    print("Initializing AI model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    try:
        # Try Granite first
        tokenizer = AutoTokenizer.from_pretrained(primary_model_path)
        if device == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            model = AutoModelForCausalLM.from_pretrained(
                primary_model_path,
                quantization_config=quantization_config,
                device_map="auto",
                torch_dtype=torch.float16
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                primary_model_path,
                torch_dtype=torch.float32
            )
            model.to(device)
        print("✅ Granite model initialized successfully!")
        return True

    except Exception as e:
        print(f"⚠ Error initializing Granite: {e}")
        print("Falling back to smaller model...")

        # Fallback model
        try:
            tokenizer = AutoTokenizer.from_pretrained(fallback_model_path)
            model = AutoModelForCausalLM.from_pretrained(fallback_model_path)
            model.to(device)
            print("✅ Fallback model initialized successfully!")
            return True
        except Exception as e2:
            print(f"❌ Error initializing fallback model: {e2}")
            print("Running with dummy responses only.")
            return False

def generate_response(question):
    """Generate response using available AI model"""
    global tokenizer, model, device

    if model is None or tokenizer is None:
        return "I'm currently setting up my AI capabilities. Please try again in a moment."

    try:
        prompt = f"""You are a helpful AI assistant for a government citizen engagement platform. 
        Provide clear, accurate, and helpful information about government services, policies, and civic processes.

        Question: {question}

        Answer:"""

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        inputs = inputs.to(device)

        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.1
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "Answer:" in response:
            response = response.split("Answer:")[-1].strip()

        return response

    except Exception as e:
        print(f"Error generating response: {e}")
        return "I’m having technical difficulties right now. Please try again later."

def analyze_sentiment(text):
    """Simple sentiment analysis function"""
    text_lower = text.lower()

    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                      'perfect', 'outstanding', 'brilliant', 'superb', 'satisfied',
                      'happy', 'pleased', 'impressed', 'helpful', 'efficient']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing',
                      'frustrated', 'angry', 'upset', 'poor', 'inadequate', 'useless',
                      'slow', 'delayed', 'problem', 'issue', 'complaint']

    positive_score = sum(1 for word in positive_words if word in text_lower)
    negative_score = sum(1 for word in negative_words if word in text_lower)

    if positive_score > negative_score:
        return 'Positive'
    elif negative_score > positive_score:
        return 'Negative'
    else:
        return 'Neutral'

# ------------------- ROUTES -------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/chat')
def chat():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    question = request.form.get('question', '').strip()
    if not question:
        return render_template('chat.html', error="Please enter a question.")

    response = generate_response(question)

    chat_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'question': question,
        'response': response
    }
    chat_history.append(chat_entry)

    return render_template('chat.html', question_response=response, user_question=question)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    feedback_text = request.form.get('feedback', '').strip()
    if not feedback_text:
        return render_template('chat.html', error="Please enter feedback text.")

    sentiment = analyze_sentiment(feedback_text)
    sentiment_key = sentiment.lower()
    if sentiment_key in sentiment_data:
        sentiment_data[sentiment_key] += 1

    return render_template('chat.html', sentiment=sentiment, feedback_text=feedback_text)

@app.route('/concern', methods=['POST'])
def submit_concern():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    concern_text = request.form.get('concern', '').strip()
    if not concern_text:
        return render_template('chat.html', error="Please enter your concern.")

    concern_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'text': concern_text,
        'status': 'Open'
    }
    concerns.append(concern_entry)

    return render_template('chat.html', concern_submitted=True)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    recent_concerns = concerns[-10:] if concerns else []
    return render_template('dashboard.html',
                           sentiment_data=sentiment_data,
                           recent_concerns=recent_concerns,
                           total_interactions=len(chat_history))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ------------------- MAIN -------------------

if __name__ == '__main__':
    print("Starting CitizenAI Application...")

    try:
        model_initialized = initialize_model()
        if not model_initialized:
            print("⚠ Running with fallback or dummy responses only.")
    except Exception as e:
        print(f"Error during model initialization: {e}")
        print("Continuing with dummy responses...")

    print("Flask application starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
