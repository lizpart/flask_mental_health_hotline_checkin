from flask import Flask, request, render_template, jsonify, Response
import openai
import os
from twilio.rest import Client
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
# Initialize the Flask application
app = Flask(__name__)

# Load the OpenAI API key
openai.api_key = ('open_ai_key')

# Twilio credentials
twilio_account_sid = "twilio_account_sid"
twilio_auth_token = "twilio_auth_token"
twilio_phone_number = "twilio_phone_number"
specialist_phone_number = ('specialist_phone_number')

#Ensure to replace these dummy values with real values

# Initialize NLTK sentiment analyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

@app.route('/')
def index():
    return render_template('checkin.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the text input from the user
        user_input = request.form['user_input']

        # Log the user input
        app.logger.info(f"User input received: {user_input}")

        # Initialize OpenAI client
        openai_client = openai.OpenAI(api_key=openai.api_key)

        # Call the OpenAI API to analyze the text
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Your session has started."},
                {"role": "user", "content": user_input}
            ]
        )

        # Log the OpenAI API response
        app.logger.info(f"OpenAI API response: {response}")

        # Parse the response
        message_content = response['choices'][0]['message']['content'] if 'choices' in response and 'message' in response['choices'][0] else ''

        # Analyze the sentiment of the user input
        sentiment_score = sid.polarity_scores(user_input)
        
        # Determine the mental state based on sentiment analysis
        if sentiment_score['compound'] <= -0.1:  # Adjust threshold for a more negative compound score
            mental_state = 'depressed'
        else:
            mental_state = 'not depressed'

        # Log the determined mental state
        app.logger.info(f"Determined mental state: {mental_state}")

        # If the user is depressed, initiate a call to a specialist
        if mental_state == 'depressed':
            # Set up the Twilio client
            client = Client(twilio_account_sid, twilio_auth_token)

            # Log the initiation of the Twilio call
            app.logger.info(f"Initiating call to specialist at {specialist_phone_number}")

            # Place a call to the specialist
            call = client.calls.create(
                to=specialist_phone_number,
                from_=twilio_phone_number,
                url=request.url_root + 'twiml' # Updated URL to point to the localhost TwiML route
            )

            # Log the Twilio call response
            app.logger.info(f"Twilio call initiated: {call.sid}")

        # Return the analysis result
        return jsonify({'mental_state': mental_state})
    except Exception as e:
        # Log any exceptions that occur
        app.logger.error(f"An error occurred: {e}")
        # Return a JSON response indicating an error
        return jsonify({'error': str(e)}), 500

@app.route('/twiml', methods=['GET'])
def twiml():
    """Respond to incoming requests."""
    twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">Hello, this is a call from the Mental Health Check-In app. A user has been flagged as needing immediate attention. </Say>
</Response>'''
    return Response(twiml_response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True)
