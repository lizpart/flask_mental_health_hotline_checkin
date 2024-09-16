from flask import Flask, request, render_template, jsonify, Response
import openai
import os
from twilio.rest import Client
from transformers import pipeline
from dotenv import load_dotenv 
import json  # Add this import

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Load the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Twilio credentials
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
user_phone_number = os.getenv('USER_PHONE_NUMBER')

# Initialize emotion classifier
classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")

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

        # Use the emotion classifier
        classification = classifier(user_input)[0]
        emotion = classification['label']
        score = classification['score']

        # Log the raw classification result
        app.logger.info(f"Raw classification: Emotion={emotion}, Score={score}")

        # Determine the mental state based on emotion
        if emotion in ['sadness', 'fear', 'anger']:
            mental_state = 'potentially depressed'
        elif emotion == 'surprise':
            mental_state = 'experiencing mood changes'
        else:  # joy or love
            mental_state = 'not showing signs of depression'

        # Log the determined mental state
        app.logger.info(f"Determined mental state: {mental_state}")

        # Initialize OpenAI client
        openai_client = openai.OpenAI(api_key=openai.api_key)

        # Call the OpenAI API to provide a response and resources
        system_message = """You are a helpful mental health assistant. Provide a supportive response and suggest appropriate resources based on the user's mental state and detected emotion. 
        If the user is potentially depressed (emotions: sadness, fear, anger) or expressing suicidal thoughts, be extra careful, supportive, and urgent in your response. Strongly encourage seeking immediate professional help.
        If the user is experiencing mood changes (emotion: surprise), offer empathetic support, gentle encouragement, and self-care tips.
        If the user is not showing strong signs of depression (emotions: joy, love), provide positive reinforcement and general mental wellness advice.
        Include links to at least two reputable articles about mental health and two exercises that can help with the user's current state. 
        Structure your response with clear sections for 'Response', 'Helpful Articles', and 'Exercises to Try', but use plain text formatting."""

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"The user said: {user_input}. The detected emotion is: {emotion}. The mental state was determined to be: {mental_state}"}
            ]
        )

        
        # Parse the OpenAI response
        ai_response = response.choices[0].message.content

        # Log the parsed AI response
        app.logger.info(f"Parsed AI response: {ai_response}")

        # Initialize the result dictionary
        result = {
            'emotion': emotion,
            'mental_state': mental_state,
            'ai_response': ai_response
        }

        # If the user is potentially depressed, initiate a Twilio voice call
        if mental_state == 'potentially depressed':
            if user_phone_number:
                try:
                    client = Client(twilio_account_sid, twilio_auth_token)
                    
                    call = client.calls.create(
                        to=user_phone_number,
                        from_=twilio_phone_number,
                        url=request.url_root + 'twiml'
                    )
                    
                    app.logger.info(f"Twilio call initiated: {call.sid}")
                    result['twilio_call_status'] = 'initiated'
                except Exception as twilio_error:
                    app.logger.error(f"Twilio call failed: {str(twilio_error)}")
                    result['twilio_call_status'] = 'failed'
            else:
                app.logger.error("Twilio call not initiated: user_phone_number is not set")
                result['twilio_call_status'] = 'not initiated - missing phone number'

        return jsonify(result)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/twiml', methods=['GET'])
def twiml():
    twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">Hello, this is a message from the Mental Health Check-In app. We've noticed that you might be going through a difficult time. Please remember that help is available. Consider reaching out to a mental health professional or a trusted friend. You can also call the National Suicide Prevention Lifeline at 1-800-273-8255 for immediate support. We care about your well-being and encourage you to seek help if needed.</Say>
</Response>'''
    return Response(twiml_response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True)
