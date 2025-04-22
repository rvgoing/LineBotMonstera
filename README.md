# FoliageFsx Line Bot AI

This project is a Line Bot AI application designed to assist with plant care and diagnostics. It uses Flask as the web framework and integrates with the Line Messaging API to provide interactive features for users. The bot can classify plant images, manage plant care profiles, and send reminders for plant care tasks.

## Purpose

The primary goal of this project is to empower plant enthusiasts and gardeners with expert advice and innovative tools for nurturing Monstera and other landscape plants. By offering tailored guidance, pest management solutions, and damage control strategies, this project ensures that users can maintain the health, vibrancy, and aesthetic appeal of their plants. Whether you're a seasoned horticulturist or a beginner, this platform is designed to make plant care an engaging and rewarding experience.

## Features

- **Plant Image Classification**: Uses a pre-trained TensorFlow model to classify plant images into categories such as healthy, root rot, sunburn, etc.
- **Plant Care Profiles**: Allows users to set and view plant care parameters like height, age, environment, and pot settings.
- **Reminders**: Users can set reminders for watering, fertilizing, cleaning leaves, and repotting plants.
- **Quick Replies**: Provides quick reply options for easy interaction.
- **Image Upload**: Supports uploading plant images for classification or record-keeping. Advanced usage includes leveraging user feedback to improve the model's precision. When a user provides a new image that can definitively rectify a specific class, the system incorporates this data to retrain the model, resulting in an improved version.

## Requirements

- Python 3.7+
- TensorFlow
- Flask
- Line Messaging API SDK
- APScheduler
- PIL (Pillow)
- pytz

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd FoliageFsx
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for Line Messaging API:
   - `LINE_CHANNEL_SECRET`: Your Line channel secret.
   - `LINE_CHANNEL_ACCESS_TOKEN`: Your Line channel access token.

4. Place the pre-trained TensorFlow model (`generator_v2.h5`) in the appropriate directory.

## Usage

1. Start the Flask server:
   ```bash
   python LineBotAI.py
   ```

2. Expose the server to the internet using a tool like ngrok (optional):
   ```bash
   ngrok http 5000
   ```

3. Set the callback URL in the Line Developer Console to your server's public URL (e.g., `https://<ngrok-url>/callback`).

## File Structure

- `LineBotAI.py`: Main application file.
- `requirements.txt`: Python dependencies.
- `Procfile`: Configuration for deployment (e.g., Heroku).

## Key Components

### Flask API
- Handles incoming requests from the Line Messaging API.
- Routes:
  - `/callback`: Main webhook endpoint for Line events.

### TensorFlow Model
- Pre-trained model for classifying plant images.
- Located at `/content/drive/MyDrive/generator_v2.h5` (update the path as needed).

### Line Messaging API
- Sends and receives messages from users.
- Supports text, image, and postback events.

### APScheduler
- Schedules reminders for plant care tasks.


### APScheduler
- Schedules reminders for plant care tasks.

## Quick Reply Options
- Provides interactive buttons for users to select plant care parameters.

## Reminders
- Users can set reminders for:
  - Watering
  - Fertilizing
  - Cleaning leaves
  - Repotting

## Deployment

1. Deploy to a cloud platform like Heroku or AWS.
2. Use the `Procfile` for Heroku deployment.
3. Ensure the server is accessible via a public URL.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- TensorFlow for the machine learning model.
- Line Messaging API for the chatbot platform.
- Flask for the web framework.