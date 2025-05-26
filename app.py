import streamlit as st
import easyocr
from pdf2image import convert_from_bytes
from PIL import Image
import numpy as np
import tempfile
import os

# Setup EasyOCR reader
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

st.title("📄 PDF Invoice OCR Extractor")
st.markdown("Upload scanned or image-based PDF invoices to extract text using OCR.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Converting PDF pages to images..."):
        images = convert_from_bytes(uploaded_file.read(), dpi=300)

    extracted_text = ""
    for i, image in enumerate(images):
        st.image(image, caption=f"Page {i+1}", use_column_width=True)
        np_image = np.array(image)

        with st.spinner(f"🔍 Performing OCR on Page {i+1}..."):
            result = reader.readtext(np_image, detail=0, paragraph=True)
            page_text = "\n".join(result)
            extracted_text += f"\n--- Page {i+1} ---\n{page_text}\n"

    st.subheader("📝 Extracted Text")
    st.text_area("Result", value=extracted_text, height=300)

    # Download button
    st.download_button(
        label="💾 Download as .txt",
        data=extracted_text,
        file_name="invoice_text_output.txt",
        mime="text/plain"
    )
