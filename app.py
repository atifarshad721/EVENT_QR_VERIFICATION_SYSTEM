from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os
import pywhatkit
from datetime import datetime, time
import secrets
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///participants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'qrcodes'
db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    qr_code = db.Column(db.String(100), nullable=False)
    unique_id = db.Column(db.String(8), nullable=False, unique=True)  # Ensure NOT NULL and UNIQUE

def generate_unique_id():
    alphabet = string.ascii_letters + string.digits
    while True:
        unique_id = ''.join(secrets.choice(alphabet) for _ in range(8))
        if not Participant.query.filter_by(unique_id=unique_id).first():
            return unique_id

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/participants')
def participants():
    participants = Participant.query.all()
    return render_template('participants.html', participants=participants)

# Modify the register route
@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        phone = request.form['phone']
        
        # Generate unique ID
        unique_id = generate_unique_id()
        qr_filename = f"{unique_id}.png"
        
        # Create participant
        participant = Participant(
            name=name, 
            phone=phone,
            unique_id=unique_id,
            qr_code=qr_filename
        )
        db.session.add(participant)
        db.session.commit()

        # Generate QR code
        qr_data = f"ID: {unique_id}\nName: {name}\nPhone: {phone}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        full_img_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)
        img.save(full_img_path)
        
        # Verify QR code file
        if not os.path.exists(full_img_path):
            raise FileNotFoundError(f"QR code file not found: {full_img_path}")

        # Clean phone number
        # cleaned_phone = phone.strip().replace('+', '').replace(' ', '')
        
        # Send WhatsApp message
        message = f'Hello {name}! Here is your QR code for the event. Please keep it safe and present it at the event. (This is an automated message. Please do not reply.)'
        
        # Send text message
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=15,
            tab_close=False
        )

        # Wait for message to send
        # time.sleep(10)  # Add delay to ensure message is sent
        
        # Send QR code image
        pywhatkit.sendwhats_image(
            receiver=phone,
            img_path=full_img_path,
            caption="Your Event QR Code",
            wait_time=20,  # Increased wait time
            tab_close=False
        )

        return redirect(url_for('participants'))
        
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}", 500

@app.route('/verify_qr', methods=['POST'])
def verify_qr():
    qr_data = request.form['qr_data']
    try:
        # Find ID line safely
        id_lines = [line for line in qr_data.split('\n') if line.startswith('ID: ')]
        
        if not id_lines:
            return "❌ Invalid QR format: Missing ID field"
            
        unique_id = id_lines[0].split('ID: ')[1].strip()
        
        # Check database
        participant = Participant.query.filter_by(unique_id=unique_id).first()
        
        if participant:
            return f"✅ Verified: {participant.name} (ID: {participant.unique_id})"
        return "❌ Verification failed: ID not found"

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')

@app.route('/qrcodes/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)