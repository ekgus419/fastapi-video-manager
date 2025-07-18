# 베이스 이미지 선택 (안정적인 일반 버전)
FROM python:3.11

# 컨테이너 안에서 작업할 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 (pip install을 먼저 하기 위함)
COPY requirements.txt .

# pip으로 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# netcat 설치
RUN apt-get update && apt-get install -y netcat-traditional

# 나머지 소스코드 전체 복사
COPY . .

# FastAPI 앱 실행 명령 (서버 실행용)
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
