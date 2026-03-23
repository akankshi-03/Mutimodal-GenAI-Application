import streamlit as st
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering

st.set_page_config(page_title="Multimodal VQA App", layout="centered")

st.title("🧠 Multimodal AI: Image Q&A")
st.write("Upload an image and ask multiple questions about it!")

@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
    return processor, model

processor, model = load_model()

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # session state for chat
    if "history" not in st.session_state:
        st.session_state.history = []

    question = st.text_input("Ask your question:")

    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking... 🤔"):
                inputs = processor(image, question, return_tensors="pt")
                out = model.generate(**inputs)
                answer = processor.decode(out[0], skip_special_tokens=True)

            st.session_state.history.append((question, answer))

    # show history
    for q, a in st.session_state.history:
        st.write(f"❓ {q}")
        st.write(f"✅ {a}")
