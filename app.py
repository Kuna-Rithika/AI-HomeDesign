import streamlit as st
import google.generativeai as genai
import requests

# --- Configure the API key for the Gemini API ---
api_key = "AIzaSyDtwBvm4ac-ggpkZahy4727sf21FI_aOpA"

genai.configure(api_key=api_key)

# --- Configure the model generation settings ---
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# --- Function to generate home design ideas ---
def generate_design_idea(style, size, rooms):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    context = (
        f"Create a custom home design plan with the following details:\n"
        f"Style: {style}\n"
        f"Size: {size}\n"
        f"Rooms: {rooms}\n"
        "Include layout suggestions, color schemes, and furniture recommendations. "
        "Format the output in Markdown."
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [context],
            },
        ]
    )

    response = chat_session.send_message(context)
    if isinstance(response.candidates[0].content, str):
        text = response.candidates[0].content
    else:
        text = response.candidates[0].content.parts[0].text

    return text

# --- Function to fetch image from Lexica.art ---
def fetch_image_from_lexica(style):
    lexica_url = f"https://lexica.art/api/v1/search?q={style}"
    response = requests.get(lexica_url)
    data = response.json()
    if data.get('images'):
        return data['images'][0]['src']  # First image URL
    return None

# --- Streamlit UI ---
st.title("🏡 Home Design AI")

style = st.text_input("Enter home style (e.g., Modern, Rustic):")
size = st.text_input("Enter home size (e.g., 2000 sq ft):")
rooms = st.number_input("Enter number of rooms:", min_value=1, step=1)

if st.button("Generate Design"):
    if style and size and rooms:
        design_text = generate_design_idea(style, size, rooms)
        st.subheader("AI Generated Home Design")
        st.markdown(design_text)

        image_url = fetch_image_from_lexica(style)
        if image_url:
            st.image(image_url, caption=f"{style} Style Example")
        else:
            st.info("No example image found for this style.")
    else:
        st.warning("Please fill all fields before generating.")
