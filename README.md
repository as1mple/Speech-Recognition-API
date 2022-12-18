# MongoDB-Template
- - - 
## RUN MONGO

```bash
docker-compose up -d
```

## RUN FastAPI

```bash
pip install -r requirements.txt
```

```bash
export HOST=YOUR-HOST
export PORT=YOUR-PORT
export USERNAME=YOUR-USERNAME
export PASSWORD=YOUR-PASSWORD
```
 = os.getenv("MONGO_HOST")
 = os.getenv("MONGO_PORT")  
 = os.getenv("MONGO_USERNAME")
 = os.getenv("MONGO_PASSWORD")


```bash
uvicorn src.api_run:app --h11-max-incomplete-event-size 100000000
```

## RUN DOCKER

```bash
sudo docker build -t fastapi_mongo -f Dockerfile . # => Docker build
```
```bash
sudo docker run -p 8080:5011 -e HOST=YOUR-HOST -e PORT=YOUR-PORT -e USERNAME=YOUR-USERNAME -e PASSWORD=YOUR-PASSWORD fastapi_mongo # => Docker run
```