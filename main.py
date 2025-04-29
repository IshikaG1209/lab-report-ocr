from fastapi import FastAPI, UploadFile, File
import pytesseract
from PIL import Image
import shutil
import os
import re

app = FastAPI()

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.get("/")
def home():
    return {"message": "Lab Report OCR API is running"}

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Image.open(file.filename)
    text = pytesseract.image_to_string(image)
    os.remove(file.filename)

    lines = text.split('\n')
    lab_results = []

    pattern = re.compile(r"(?P<test>[A-Za-z\s]+)\s+(?P<value>\d+\.?\d*)\s*(?P<unit>[a-zA-Z%\/]*)\s*(?P<range>\d+[-–]\d+\.?\d*)?")

    for line in lines:
        match = pattern.search(line)
        if match:
            lab_results.append({
                "test_name": match.group("test").strip(),
                "value": match.group("value"),
                "unit": match.group("unit"),
                "reference_range": match.group("range") if match.group("range") else "N/A"
            })

    return {"lab_tests": lab_results}
