FROM python:3.13.3-slim
WORKDIR /app
COPY main.py /app/
CMD ["python", "main.py"]
