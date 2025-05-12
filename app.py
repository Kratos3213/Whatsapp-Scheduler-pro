from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whatsapp_scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Twilio client setup
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    recipient = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add login logic here
        pass
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    messages = Message.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', messages=messages)

@app.route('/schedule', methods=['POST'])
@login_required
def schedule_message():
    data = request.json
    message = Message(
        content=data['content'],
        scheduled_time=datetime.fromisoformat(data['scheduled_time']),
        recipient=data['recipient'],
        user_id=current_user.id,
        is_recurring=data.get('is_recurring', False),
        recurrence_pattern=data.get('recurrence_pattern')
    )
    db.session.add(message)
    db.session.commit()
    
    # Schedule the message
    scheduler.add_job(
        send_whatsapp_message,
        'date',
        run_date=message.scheduled_time,
        args=[message.id]
    )
    
    return jsonify({'status': 'success', 'message_id': message.id})

def send_whatsapp_message(message_id):
    message = Message.query.get(message_id)
    if message:
        try:
            twilio_client.messages.create(
                from_=f'whatsapp:{os.getenv("TWILIO_WHATSAPP_NUMBER")}',
                body=message.content,
                to=f'whatsapp:{message.recipient}'
            )
            message.status = 'sent'
        except Exception as e:
            message.status = 'failed'
        db.session.commit()

@app.route('/upload-contacts', methods=['POST'])
@login_required
def upload_contacts():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        # Process contacts here
        return jsonify({'status': 'success', 'message': 'Contacts uploaded successfully'})
    
    return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
