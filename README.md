# Mental Health Check-in App

## Introduction
This project is a Mental Health Check-in App developed using Flask, OpenAI, and Twilio Programmable Voice. The application allows users to check in on their mental health by inputting their feelings, which are then analyzed using emotion classification and natural language processing. Based on the analysis, the app provides personalized responses, resources, and in cases of potential depression, initiates an automated support call.

## Features
- User-friendly interface for inputting feelings and submitting them for analysis.
- Emotion classification using a pre-trained model.
- Integration with OpenAI's GPT model for generating personalized responses and resources.
- Automated Twilio Programmable Voice calls for users flagged as potentially depressed.
- Logging functionality to track user input, analysis results, and call initiation.
- Customizable pre-recorded message for voice calls.

## Setup
1. Clone the repository to your local machine:
   ```
   git clone https://github.com/yourusername/mental-health-checkin-app.git
   ```

2. Navigate to the project directory:
   ```
   cd mental-health-checkin-app
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up your OpenAI and Twilio accounts and obtain the necessary API keys and credentials.

6. Create a `.env` file in the project root and add your environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   PHONE_NUMBER=phone_number
   ```

7. Run the Flask application:
   ```
   python app.py
   ```

8. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage
1. Input your feelings into the provided textarea on the homepage.
2. Click the "Analyze" button to submit your input for analysis.
3. The application will display:
   - The detected emotion
   - Your current mental state
   - A personalized AI-generated response
   - Helpful articles and exercises
4. If your mental state is flagged as 'potentially depressed,' the application will initiate an automated call via Twilio.

## Customization
- You can customize the pre-recorded message for Twilio calls by modifying the TwiML response in the `/twiml` route.
- Adjust the emotion classification thresholds and mental state determination logic in the `/analyze` route as needed.

## Contributions
Contributions to the project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
