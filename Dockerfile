FROM python:3.8-slim
WORKDIR /app
RUN pip3 install flask
COPY . .
EXPOSE 8080
CMD ["python3", "app.py"]