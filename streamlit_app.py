import streamlit as st
from openai import OpenAI
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Show title and description
st.title("🍽️ Nutritional Assistant")
st.write(
    "Welcome to your personal nutritional assistant! I can help you plan meals, "
    "suggest recipes, and create weekly meal plans based on your preferences and dietary needs."
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {
        "dietary_restrictions": [],
        "allergies": [],
        "favorite_cuisines": [],
        "religious_restrictions": [],
        "email": "",
        "meal_preferences": {
            "breakfast": True,
            "lunch": True,
            "dinner": True,
            "snacks": True
        }
    }

# Sidebar for user preferences
with st.sidebar:
    st.header("User Preferences")
    
    # Dietary Restrictions
    st.subheader("Dietary Restrictions")
    dietary_options = ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Paleo"]
    st.session_state.user_preferences["dietary_restrictions"] = st.multiselect(
        "Select your dietary restrictions",
        dietary_options
    )
    
    # Allergies
    st.subheader("Allergies")
    allergy_options = ["Nuts", "Shellfish", "Eggs", "Soy", "Wheat", "Fish"]
    st.session_state.user_preferences["allergies"] = st.multiselect(
        "Select your allergies",
        allergy_options
    )
    
    # Cuisine Preferences
    st.subheader("Favorite Cuisines")
    cuisine_options = ["Italian", "Mexican", "Indian", "Chinese", "Mediterranean", "Japanese", "American"]
    st.session_state.user_preferences["favorite_cuisines"] = st.multiselect(
        "Select your favorite cuisines",
        cuisine_options
    )
    
    # Religious Restrictions
    st.subheader("Religious Restrictions")
    religious_options = ["Halal", "Kosher", "None"]
    st.session_state.user_preferences["religious_restrictions"] = st.selectbox(
        "Select your religious restrictions",
        religious_options
    )
    
    # Email for notifications
    st.subheader("Email Notifications")
    st.session_state.user_preferences["email"] = st.text_input(
        "Enter your email for daily meal plans"
    )
    
    # Meal Preferences
    st.subheader("Meal Preferences")
    st.session_state.user_preferences["meal_preferences"]["breakfast"] = st.checkbox("Breakfast", value=True)
    st.session_state.user_preferences["meal_preferences"]["lunch"] = st.checkbox("Lunch", value=True)
    st.session_state.user_preferences["meal_preferences"]["dinner"] = st.checkbox("Dinner", value=True)
    st.session_state.user_preferences["meal_preferences"]["snacks"] = st.checkbox("Snacks", value=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about nutrition, recipes, or meal planning..."):
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare context for the AI
    context = f"""
    User Preferences:
    - Dietary Restrictions: {', '.join(st.session_state.user_preferences['dietary_restrictions'])}
    - Allergies: {', '.join(st.session_state.user_preferences['allergies'])}
    - Favorite Cuisines: {', '.join(st.session_state.user_preferences['favorite_cuisines'])}
    - Religious Restrictions: {st.session_state.user_preferences['religious_restrictions']}
    - Meal Preferences: {', '.join([meal for meal, enabled in st.session_state.user_preferences['meal_preferences'].items() if enabled])}
    """

    # Generate response
    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful nutritional assistant. Use this context about the user's preferences: {context}"},
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )

        # Display assistant's response
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # If the user asked for a meal plan, send it via email
        if "meal plan" in prompt.lower() and st.session_state.user_preferences["email"]:
            send_meal_plan_email(st.session_state.user_preferences["email"], response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def send_meal_plan_email(email, meal_plan):
    """Send the meal plan via email"""
    try:
        # Email configuration from Streamlit secrets
        sender_email = st.secrets["email"]["user"]
        sender_password = st.secrets["email"]["password"]
        
        # Create message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = f"Your Daily Meal Plan - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Add body
        body = f"""
        Hello!
        
        Here's your meal plan for today:
        
        {meal_plan}
        
        Enjoy your meals!
        """
        msg.attach(MIMEText(body, "plain"))
        
        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        st.success("Meal plan sent to your email!")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
