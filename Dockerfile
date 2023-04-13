FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev libssl-dev graphviz parallel


WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache -r requirements.txt

CMD ["python3", "main.py"]
