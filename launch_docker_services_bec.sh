docker run -p 27017:27017 --name mongo-bec -d mongo
docker run --network=host --name redis-bec -d redis
#docker run --network=host --name scibec -d scibec
