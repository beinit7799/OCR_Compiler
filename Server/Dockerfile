FROM python:3.12

WORKDIR /app

# Install dependencies for opencv and dlib as docker lacks graphical libraries.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    gcc \
    g++ \
    openjdk-11-jdk \
    libopencv-dev \
    mingw-w64 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
# COPY .env ./
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
