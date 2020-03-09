export $(egrep -v '^#' .env | xargs)

docker build --tag prophetable --file docker/Dockerfile.dev . && \
    docker run --rm \
    -v $VOLUME:/data \
    --env-file .env \
    --name=pm \
    prophetable