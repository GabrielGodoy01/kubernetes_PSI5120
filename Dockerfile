# Usar uma imagem base do Python
FROM python:3.9

# Instalar dependências do sistema para operações gráficas
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Definir o diretório de trabalho dentro do container como /app
WORKDIR /app

# Copia o requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar as dependências Python listadas em requirements.txt
RUN pip install cython pillow>=7.0.0 numpy>=1.18.1 opencv-python>=4.1.2 torch>=1.9.0 --extra-index-url https://download.pytorch.org/whl/cpu torchvision>=0.10.0 --extra-index-url https://download.pytorch.org/whl/cpu pytest==7.1.3 tqdm==4.64.1 scipy>=1.7.3 matplotlib>=3.4.3 mock==4.0.3

RUN pip install imageai --upgrade

# Copiar todo o restante dos arquivos do projeto para o diretório de trabalho no container
COPY . .

# Expor a porta 8080 para acesso externo
EXPOSE 8080

# Comando padrão para iniciar a aplicação Python (app.py)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]