FROM python:3.9

WORKDIR /app

RUN apt update && apt install -y

RUN python3 -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "app:app", "--bind", "0.0.0.0:8000"]
