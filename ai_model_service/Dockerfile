FROM python:3.9

WORKDIR /app

RUN apt update && apt install -y \
    gcc \
    libffi-dev \
    openssl \
    xz-utils \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install gunicorn

COPY . .

CMD ["gunicorn", "-w", "4", "app:app", "--bind", "0.0.0.0:8000"]
