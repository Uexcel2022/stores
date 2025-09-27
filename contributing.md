# How To Run Docker Locally

docker build -t rest-apis-flask-python .

docker build -t flask-smorest-api .

docker run -p 5000:5000 rest-apis-flask-python (include -d or -dp)

docker run -dp 5000:5000 -w //app -v "%cd%://app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"

#pip install -r requirements.txt