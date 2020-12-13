# Weather-Covid-Flask
Weather/Covid API 

## Weather + Covid stats = ~knowledge~

#
Some long boring informational section why or what this app does

## Installation

Use docker pull [Docker](https://hub.docker.com/r/mikehanson/weather-flask).

```bash
docker pull mikehanson/weather-flask
```

## Usage

Variables that can be passed to docker img. 
```python
HOSTNAME        - Graylog server ip/hostname
PORT            - Graylog port (ie. 5000)
```

## Example 

```bash 

sudo docker run -p 5000:5000 -e WeatherAPIToken='OPENWEATHERAPIKEY' docker_img_name

```

## Get docker here 
https://docs.docker.com/get-docker/

## DockerHub 
[https://hub.docker.com/r/mikehanson/weather-flask](https://hub.docker.com/r/mikehanson/weather-flask)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
