from flask import Flask, request, jsonify
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

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']
        
        app.logger.debug(f"Received latitude: {latitude}, longitude: {longitude}")
        
        location_url = f"https://www.google.com/maps?q={latitude},{longitude}"
        message_body = (f"**Alert!!...serious car crash at coordinates: {latitude}, {longitude}. "
                        f"Car no [WB38-B-1234]. Emergency services are responding ASAP. "
                        f"Check the location: {location_url}")
        
        # Send the message via Twilio
        message = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=message_body,
            to='+919749650727'  # Replace with the recipient's phone number
        )

        app.logger.debug(f"Message SID: {message.sid}")

        return jsonify({'message_sid': message.sid})
    
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
