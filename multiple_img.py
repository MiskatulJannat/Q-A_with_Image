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
st.write('Upload multiple images and ask a question about them.')

# Retrieve the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Setting up the headers for OpenAI API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Streamlit file uploader to accept user's images
uploaded_images = st.file_uploader("Choose multiple images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
if uploaded_images:
    st.subheader("Uploaded Images:")
    st.image(uploaded_images, caption=[f"Image {i + 1}" for i in range(len(uploaded_images))], use_column_width=True)

    # Base64 encode all the uploaded images
    base64_images = [encode_image(img) for img in uploaded_images]

    # Text input for user's question about the images
    question = st.text_input("What is your question about these images?")

    # When the user submits a question
    if st.button('Ask'):
        if question:
            # Create a list of messages for each image
            messages = []
            for base64_image in base64_images:
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                })

            # Add the user's question as a common message for all images
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            })

            payload = {
                "model": "gpt-4-vision-preview",
                "messages": messages,
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
