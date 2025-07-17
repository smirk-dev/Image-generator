import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI
#run using python -m streamlit run app.py
# Install the required packages if not already installed
# Use your OpenAI API key
client = OpenAI(api_key="")

def generate_image(prompt, size="512x512"):
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size=size,
            n=1
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def download_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

st.set_page_config(page_title="AI Image Generator")
st.title("🧠 AI Image Generator")
st.caption("Using OpenAI's DALL·E 2")

prompt = st.text_input("Enter a prompt:")
image_size = st.selectbox("Choose Image Size", ["256x256", "512x512", "1024x1024"], index=1)

if st.button("Generate"):
    if prompt:
        with st.spinner("Generating..."):
            image_url = generate_image(prompt, image_size)
            if image_url:
                image = download_image(image_url)
                st.image(image, caption="Generated Image", use_column_width=True)
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                st.download_button("Download Image", buffered.getvalue(), file_name="generated.png", mime="image/png")
    else:
        st.warning("Please enter a prompt.")
