FROM python:3

# configure timezone
ENV TZ America/Chicago

# We copy just the requirements.txt first to leverage Docker cache
COPY . . 
COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 5000

ENV WeatherAPIToken = **None** 

CMD ["python3", "app.py"]