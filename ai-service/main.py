from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI()

model = YOLO('best.pt')

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    results = model.predict(source=image, conf=0.3)
    
    detected = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls)
            conf = float(box.conf)
            name = model.names[cls]
            detected.append({
                "name": name,
                "confidence": round(conf, 2)
            })
    
    return {"success": True, "detected": detected}