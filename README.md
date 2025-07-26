# AI Insight Snap

Turn any spreadsheet or handwritten data into instant insights! Upload an image, and the app uses OCR and AutoML to extract and analyze your data.

## Features
- No-code data analysis from images
- Instant summary statistics
- Frontend in Streamlit, backend in FastAPI

## How to Run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Start API server: `uvicorn app:app --reload`
4. Start frontend: `streamlit run frontend_app.py`
