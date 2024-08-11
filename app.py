# Antes de iniciar a aplicação deve-se fazer o Download do modelo YOLOv3:
# https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/

from fastapi import FastAPI
from imageai.Detection import ObjectDetection
import os
from fastapi.responses import JSONResponse

app = FastAPI()

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
detector.loadModel()

@app.get("/detect")
def detect_objects():
    input_image_path = os.path.join(execution_path, "sample.jpg")
    output_image_path = os.path.join(execution_path, "imagenew.jpg")

    # Realiza a detecção de objetos
    detections = detector.detectObjectsFromImage(
        input_image=input_image_path, 
        output_image_path=output_image_path, 
        minimum_percentage_probability=30
    )
    
    # Retorna os resultados da detecção
    results = [
        {
            "name": eachObject["name"],
            "percentage_probability": eachObject["percentage_probability"],
            "box_points": eachObject["box_points"]
        }
        for eachObject in detections
    ]

    # Delete image
    os.remove(output_image_path)
    
    return JSONResponse(content={"detections": results})
