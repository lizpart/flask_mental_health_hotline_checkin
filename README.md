# Mental Health Hotline Check-in App
## Introduction
This project is a Mental Health Hotline Check-in App developed using Flask, OpenAI, and Twilio Programmable Voice. The application allows users to check in on their mental health by inputting their feelings, which are then analyzed using sentiment analysis. If a user's mental state is flagged as 'depressed,' the application initiates a call to a specialist via Twilio's API for immediate support.

## Features
 - User-friendly interface for inputting feelings and submitting them for analysis.
 - Sentiment analysis of user input to determine mental state.
 - Integration with Twilio Programmable Voice to initiate calls to specialists for users in distress.
 - Use of OpenAI for natural language processing capabilities to enhance analysis accuracy.
 - Logging functionality to track user input, analysis results, and call initiation.
## Setup
1. Clone the repository to your local machine:
   `git clone https://github.com/lizpart/flask_mental_health_hotline_checkin.git`
2. Navigate to the project directory:
   `cd flask_mental_health_hotline_checkin`
3. Install the required dependencies:
    `pip install -r requirements.txt`
4. Set up your OpenAI and Twilio accounts and obtain the necessary API keys and credentials.
5. Configure the application by updating the config.py file with your API keys and credentials.
6. Run the Flask application:
   `python app.py`
7. Open a web browser and navigate to the provided URL (typically http://localhost:5000) to access the application.

## Usage
1. Input your feelings into the provided textarea on the homepage.
2. Click the "Check In" button to submit your feelings for analysis.
3. Monitor the application's response to see if your mental state is flagged as 'depressed.'
4. If flagged as 'depressed,' the application will initiate a call to a specialist via Twilio for immediate support.
   
## Contributions
Contributions to the project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License.



