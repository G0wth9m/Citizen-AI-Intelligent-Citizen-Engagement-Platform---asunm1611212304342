"""
CitizenAI Demo Version - Lightweight Testing
This version runs without heavy AI models for quick testing and demonstration.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'demo-secret-key-change-in-production'

# In-memory storage for demo
chat_history = []
sentiment_data = {'positive': 0, 'neutral': 0, 'negative': 0}
concerns = []

def demo_generate_response(question):
    """Demo response generator with predefined responses"""
    question_lower = question.lower()
    
    # Government service responses
    if any(word in question_lower for word in ['tax', 'taxes']):
        return "For tax-related inquiries, you can visit our online tax portal or contact the revenue department at 1-800-TAX-HELP. Tax filing deadlines are April 15th for individual returns."
    
    elif any(word in question_lower for word in ['license', 'permit']):
        return "You can apply for licenses and permits online through our citizen portal. Processing times vary by type: driver's licenses (1-2 weeks), business permits (2-4 weeks), building permits (4-6 weeks)."
    
    elif any(word in question_lower for word in ['vote', 'voting', 'election']):
        return "Voting information is available at your local election office. You can register to vote online, check your polling location, and view sample ballots on our election website."
    
    elif any(word in question_lower for word in ['utility', 'water', 'electric']):
        return "For utility services, contact your local utility provider. Water/sewer issues can be reported to the public works department. We also offer energy efficiency programs for residents."
    
    elif any(word in question_lower for word in ['park', 'recreation']):
        return "Our parks and recreation department offers various programs including youth sports, senior activities, and facility rentals. Visit our website to view schedules and register for programs."
    
    elif any(word in question_lower for word in ['police', 'emergency']):
        return "For emergencies, call 911. For non-emergency police matters, contact your local police department. We also offer community policing programs and safety workshops."
    
    elif any(word in question_lower for word in ['trash', 'garbage', 'recycling']):
        return "Trash collection schedules vary by neighborhood. Recycling is collected bi-weekly. For bulk item pickup, schedule online or call public works. We encourage participation in our recycling programs."
    
    elif any(word in question_lower for word in ['road', 'pothole', 'street']):
        return "Report road issues through our citizen portal or mobile app. Pothole repairs are prioritized by safety risk. Road construction schedules and detours are posted on our traffic website."
    
    elif any(word in question_lower for word in ['hello', 'hi', 'help']):
        return "Hello! I'm the CitizenAI assistant. I can help you with information about government services, permits, utilities, voting, and more. What would you like to know?"
    
    else:
        return f"Thank you for your question about '{question}'. For specific information, please contact the relevant department or visit our comprehensive citizen services portal. Our staff is available Monday-Friday, 8 AM - 5 PM to assist you."

def analyze_sentiment(text):
    """Simple sentiment analysis function"""
    text_lower = text.lower()
    
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'perfect', 'outstanding', 'brilliant', 'superb', 'satisfied', 'happy', 'pleased', 'impressed', 'helpful', 'efficient', 'fast', 'friendly', 'professional']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing', 'frustrated', 'angry', 'upset', 'poor', 'inadequate', 'useless', 'slow', 'delayed', 'problem', 'issue', 'complaint', 'rude', 'unprofessional', 'broken']
    
    positive_score = sum(1 for word in positive_words if word in text_lower)
    negative_score = sum(1 for word in negative_words if word in text_lower)
    
    if positive_score > negative_score:
        return 'Positive'
    elif negative_score > positive_score:
        return 'Negative'
    else:
        return 'Neutral'

# Routes
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
    
    # Generate demo response
    response = demo_generate_response(question)
    
    # Store in chat history
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
    
    # Analyze sentiment
    sentiment = analyze_sentiment(feedback_text)
    
    # Update sentiment counts
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
    
    # Store concern
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
    
    # Get recent concerns (last 10)
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
        
        # Demo authentication
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful! Welcome to CitizenAI Demo.', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Invalid credentials. Use admin/password for demo.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. Thank you for using CitizenAI!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 CitizenAI Demo Application Starting...")
    print("=" * 50)
    print("📍 URL: http://localhost:5000")
    print("👤 Demo Login: admin / password")
    print("💡 This is a lightweight demo version")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
