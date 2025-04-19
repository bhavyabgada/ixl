# Nutritional Assistant

A Streamlit application that serves as a personal nutritional assistant, helping users plan meals, suggest recipes, and create weekly meal plans based on their preferences and dietary needs.

## Features

- Personalized meal planning based on user preferences
- Dietary restrictions and allergy considerations
- Religious and cultural dietary requirements support
- Favorite cuisine preferences
- Daily meal plan email notifications
- Recipe suggestions
- Interactive chat interface

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.streamlit/secrets.toml` file with your credentials:
   ```toml
   [email]
   user = "your_email@gmail.com"
   password = "your_app_specific_password"

   [OPENAI_API_KEY]
   key = "your_openai_api_key"
   ```
4. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## Email Setup

To enable email notifications:
1. Use a Gmail account
2. Enable 2-factor authentication
3. Generate an App Password:
   - Go to Google Account Settings
   - Security > 2-Step Verification
   - App Passwords
   - Generate a new app password for "Mail"
4. Add your email credentials to the `.streamlit/secrets.toml` file

## Usage

1. Open the application in your browser
2. Set your preferences in the sidebar:
   - Dietary restrictions
   - Allergies
   - Favorite cuisines
   - Religious restrictions
   - Meal preferences
   - Email for notifications
3. Start chatting with the assistant about:
   - Meal planning
   - Recipe suggestions
   - Nutritional advice
   - Weekly meal schedules

## Contributing

Feel free to submit issues and enhancement requests!
