from flask import Flask, request, jsonify, send_from_directory
from twilio.rest import Client
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Your Twilio credentials (replace with your actual credentials)
account_sid = 'AC8693be8b9ae871b5b2bcf8ec958431c9'
auth_token = 'da0dc7fe1c69414779f045d417645ef7'
messaging_service_sid = 'MG1e29f9d5aa2ce5decdae4cdaa5be1623'
client = Client(account_sid, auth_token)

# Twilio phone details
TWILIO_PHONE_NUMBER = "+12568278549"
USER_PHONE_NUMBER = "+919749650727"

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not latitude or not longitude:
            raise ValueError("Latitude and Longitude are required")

        app.logger.debug(f"Received latitude: {latitude}, longitude: {longitude}")

        location_url = f"https://www.google.com/maps?q={latitude},{longitude}"
        message_body = (f"**Alert!!...serious car crash at coordinates: {latitude}, {longitude}. "
                        f"Car no [WB38-B-1234]. Emergency services are responding ASAP. "
                        f"Check the location: {location_url}")

        # Send the message via Twilio
        message = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=message_body,
            to=USER_PHONE_NUMBER
        )

        app.logger.debug(f"Message SID: {message.sid}")

        return jsonify({'message_sid': message.sid})

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
