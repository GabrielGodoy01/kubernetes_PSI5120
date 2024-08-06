# Usar uma imagem base do Python
FROM python:3.9

# Instalar dependências do sistema para operações gráficas
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Definir o diretório de trabalho dentro do container como /app
WORKDIR /app

# Copiar o arquivo de requisitos para o diretório de trabalho no container
COPY requirements.txt .

# Instalar as dependências Python listadas em requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o restante dos arquivos do projeto para o diretório de trabalho no container
COPY . .

# Expor a porta 8080 para acesso externo
EXPOSE 8080

# Comando padrão para iniciar a aplicação Python (app.py)
CMD ["python", "app.py"]