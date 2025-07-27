import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import io
import plotly.express as px
from pycaret.regression import setup, compare_models, pull

# Optional: set Tesseract language
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Update if needed
OCR_LANGUAGES = {"English": "eng", "Hindi": "hin", "French": "fra", "German": "deu"}

st.set_page_config(page_title="AI Insight Snap", layout="wide")

# --- Sidebar ---
st.sidebar.title("AI Insight Snap")
st.sidebar.markdown("Turn Any Data into Instant Insights – Just Snap & Analyze!")

lang_choice = st.sidebar.selectbox("OCR Language", list(OCR_LANGUAGES.keys()))
ocr_lang = OCR_LANGUAGES[lang_choice]

# --- Main Content ---
st.title("📸 Upload Your Data Image")
uploaded_file = st.file_uploader("Upload an image (e.g. table, handwritten data)", type=["png", "jpg", "jpeg"])

def parse_text_to_dataframe(text):
    lines = text.strip().split('\n')
    rows = [line.strip().split() for line in lines if line.strip()]
    df = pd.DataFrame(rows)
    # Attempt to fix columns
    try:
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
        df = df.apply(pd.to_numeric, errors='ignore')
    except:
        pass
    return df

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR
    st.subheader("🔍 Extracting Text...")
    extracted_text = pytesseract.image_to_string(image, lang=ocr_lang)
    st.text_area("OCR Output", extracted_text, height=150)

    # Parse Text into DataFrame
    st.subheader("📊 Converted Data Table")
    df = parse_text_to_dataframe(extracted_text)
    st.dataframe(df)

    # AutoML with PyCaret
    try:
        if df.shape[1] >= 2:
            st.subheader("⚙️ AutoML Insights")
            target = st.selectbox("Select Target Column", df.columns)

            with st.spinner("Running AutoML..."):
                setup(df, target=target, silent=True, verbose=False, session_id=123)
                best_model = compare_models()
                leaderboard = pull()
                st.write("Top Models:")
                st.dataframe(leaderboard)

                st.success(f"Best model: {str(best_model)}")
        else:
            st.warning("Please upload data with at least 2 columns for AutoML.")

    except Exception as e:
        st.error(f"AutoML failed: {str(e)}")

    # Plotting
    try:
        st.subheader("📈 Data Visualizations")
        x_axis = st.selectbox("Select X-Axis", df.columns)
        y_axis = st.selectbox("Select Y-Axis", df.columns)

        fig = px.line(df, x=x_axis, y=y_axis, title="Data Trend")
        st.plotly_chart(fig)
    except Exception as e:
        st.warning("Plotting skipped due to error or data mismatch.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for Data Snapshots • [GitHub](https://github.com/) • [Gumroad](https://gumroad.com/)")
