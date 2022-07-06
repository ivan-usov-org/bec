if [ "$( docker container inspect -f '{{.State.Status}}' mongo-bec )" == "running" ]; then
	echo "container mongo-bec is running"
else
	docker run -p 27017:27017 --name mongo-bec -d mongo
fi

if [ "$( docker container inspect -f '{{.State.Status}}' redis-bec )" == "running" ]; then
        echo "container redis-bec is running"
else
        docker run --network=host --name redis-bec -d redis
fi

if [ "$( docker container inspect -f '{{.State.Status}}' scibec )" == "running" ]; then
        echo "container scibec is running"
else
	docker build -t scibec -f ./scibec/Dockerfile .
        docker run --network=host --name scibec -d scibec
fi

