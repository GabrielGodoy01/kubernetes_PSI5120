# Antes de iniciar a aplicação, faça o download do modelo YOLOv3:
# https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/

from fastapi import FastAPI
from imageai.Detection import ObjectDetection
import os
from fastapi.responses import JSONResponse

# Inicializa a aplicação FastAPI
app = FastAPI()

# Obtém o caminho atual de execução do script
execution_path = os.getcwd()

# Cria uma instância do detector de objetos usando ImageAI
detector = ObjectDetection()
# Define o tipo de modelo como YOLOv3
detector.setModelTypeAsYOLOv3()
# Define o caminho para o modelo YOLOv3 previamente baixado
detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
# Carrega o modelo na memória para uso na detecção de objetos
detector.loadModel()

# Define o endpoint HTTP GET "/detect" que será acessado para detecção de objetos
@app.get("/detect")
def detect_objects():
    # Define o caminho para a imagem de entrada que será analisada
    input_image_path = os.path.join(execution_path, "sample.jpg")
    # Define o caminho para a imagem de saída, onde a detecção será marcada
    output_image_path = os.path.join(execution_path, "imagenew.jpg")

    # Realiza a detecção de objetos na imagem de entrada e salva a imagem de saída com as marcações
    detections = detector.detectObjectsFromImage(
        input_image=input_image_path, 
        output_image_path=output_image_path, 
        minimum_percentage_probability=30  # Define a probabilidade mínima para que um objeto seja considerado detectado
    )
    
    # Processa os resultados da detecção e organiza em um formato JSON
    results = [
        {
            "name": eachObject["name"],  # Nome do objeto detectado
            "percentage_probability": eachObject["percentage_probability"],  # Probabilidade de acerto da detecção
            "box_points": eachObject["box_points"]  # Coordenadas da caixa delimitadora do objeto na imagem
        }
        for eachObject in detections
    ]

    # Remove a imagem de saída após a detecção (opcional, dependendo da necessidade)
    os.remove(output_image_path)
    
    # Retorna os resultados da detecção como uma resposta JSON
    return JSONResponse(content={"detections": results})
