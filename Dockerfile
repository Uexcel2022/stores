
#Deployment with Docker Container
#FROM python:3.13
#LABEL authors="excel"
#EXPOSE 5000
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#RUN pip install flask
#COPY . .
#CMD ["flask", "run", "--host","0.0.0.0"]


# Deployment with gunicorn
FROM python:3.13
LABEL authors="excel"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install flask
COPY . .
CMD ["gunicorn", "--bind","0.0.0.0:80","app:create_app()"]

