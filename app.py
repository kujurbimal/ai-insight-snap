from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import pandas as pd
import io

app = FastAPI()

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    raw_text = pytesseract.image_to_string(image)
    
    try:
        df = pd.read_csv(io.StringIO(raw_text))
        stats = df.describe(include='all').to_dict()
        return {"dataframe": df.to_dict(), "summary": stats}
    except Exception:
        return {"error": "Could not parse image into structured data"}
