# 백엔드 이미지 빌드
FROM python:3.9 AS backend

WORKDIR /app

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# React 빌드 파일 복사
COPY . /app 

# Expose the port FastAPI will run on
EXPOSE 8080

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
