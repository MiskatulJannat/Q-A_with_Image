import streamlit as st
import requests
import base64
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to encode the image to base64
def encode_image(uploaded_image):
    return base64.b64encode(uploaded_image.getvalue()).decode('utf-8')

# Streamlit app layout
st.title('Grow with Data - Image Q&A Chat')
st.write('Upload an image and ask any question about it.')

# Retrieve the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Setting up the headers for OpenAI API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Streamlit file uploader to accept user's image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    # Display the uploaded image
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    # Base64 encode the uploaded image
    base64_image = encode_image(uploaded_image)

    # Text input for user's question about the image
    question = st.text_input("What is your question about this image?")

    # When the user submits a question
    if st.button('Ask'):
        if question:
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": question
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            # Sending post request to OpenAI API
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            # If the response is successful, display the answer
            if response.status_code == 200:
                response_data = response.json()

                # Extracting the answer from the response data
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    message_content = response_data['choices'][0]['message']['content']
                    st.write("AI:", message_content)
                else:
                    st.write("Error: No choices in the response.")
            else:
                st.write("Error:", response.json())
        else:
            st.write("Please ask a question.")

