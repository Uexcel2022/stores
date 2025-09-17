FROM python:3.13
LABEL authors="excel"
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install flask
COPY . .
CMD ["flask", "run", "--host","0.0.0.0"]

#docker build -t rest-apis-flask-python .

# docker build -t flask-smorest-api .

# docker run -p 5000:5000 rest-apis-flask-python (include -d or -dp)

# docker run -dp 5000:5000 -w //app -v "%cd%://app" flask-smorest-api  - 4 working directing with docker container
