import streamlit as st
from PIL import Image
import os
from cal import estimate_calories

# Set up the Streamlit app
st.title("Calorie Counter")
st.write("Upload an image of food to estimate its calorie content.")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

# Prompt input
prompt = st.text_input("Enter a prompt for calorie estimation", value="Estimate the calories in this food item.")

# Process the uploaded image
if uploaded_file is not None:
    try:
        # Load the image
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Automatically estimate calories after image upload
        calorie_estimate = estimate_calories(prompt, img)
        st.success(f"Calorie Estimate: {calorie_estimate}")
    except Exception as e:
        st.error(f"Error: {e}")