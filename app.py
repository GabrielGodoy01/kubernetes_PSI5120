# Importa as classes Flask, jsonify e request do módulo Flask
from flask import Flask, jsonify, request

# Importa o pacote NumPy para manipulação de arrays
import numpy as np

# Importa o OpenCV para manipulação de imagens
import cv2

# Importa o módulo base64 para decodificação de dados base64
import base64

# Importa o modelo pré-treinado ResNet50 da biblioteca Keras
from keras.applications.resnet50 import ResNet50

# Importa o módulo de pré-processamento de imagens da Keras
from keras.preprocessing import image

# Importa as funções de pré-processamento e decodificação de predições do ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions


# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Define uma rota na raiz ("/") que aceita somente requisições POST
@app.route("/", methods=['POST'])
def hello():
    # Função que será executada quando uma requisição POST for recebida na rota "/"
    
    # Exibe uma mensagem no console indicando o início da execução do modelo
    print('Começando execução do modelo')
    
    # Carrega o modelo pré-treinado ResNet50 com os pesos treinados no dataset ImageNet
    model = ResNet50(weights='imagenet')

    # Obtém a string base64 da imagem enviada na requisição (ou None se não houver)
    base64_string = request.json.get('image', None)

    # Se a string base64 for None, retorna uma resposta JSON com uma mensagem de erro
    if base64_string is None:
        return jsonify({'error': 'No image data found'})

    # Decodifica a string base64 para dados de imagem binários
    img_data = base64.b64decode(base64_string)
    
    # Converte os dados binários para um array NumPy de tipo uint8
    np_arr = np.frombuffer(img_data, np.uint8)

    # Decodifica o array NumPy em uma imagem usando OpenCV, assumindo que a imagem é colorida
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Redimensiona a imagem para 224x224 pixels, que é o tamanho de entrada esperado pelo modelo ResNet50
    img = cv2.resize(img, (224, 224))

    # Converte a imagem em um array NumPy de formato de array de imagem Keras
    x = image.img_to_array(img)

    # Adiciona uma dimensão extra ao array para representar o batch size, necessário para a predição
    x = np.expand_dims(x, axis=0)

    # Pré-processa o array de imagem de entrada de acordo com o que o modelo espera
    x = preprocess_input(x)

    # Faz a predição utilizando o modelo ResNet50
    predictions = model.predict(x)

    # Decodifica e imprime as top 3 predições, exibindo a classe e a confiança
    print(decode_predictions(predictions, top=3))

    # Decodifica as predições e pega apenas as top 3
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    # Cria uma lista de dicionários contendo o ID da classe, nome da classe e a pontuação de confiança para cada predição
    result = [{'class_id': pred[0], 'class_name': pred[1], 'score': float(pred[2])} for pred in decoded_predictions]

    # Retorna as predições em formato JSON como resposta
    return jsonify({'Predicted': result})

# Inicia o servidor Flask, disponível em todas as interfaces de rede na porta 8080, com o modo de debug ativado
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
