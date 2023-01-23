FROM python:3
WORKDIR /usr/src/app
COPY . .
ENV DB_HOST=mongodb
ENV REDIS_HOST=redis
RUN pip install -r requirements.txt