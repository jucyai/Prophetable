export $(egrep -v '^#' .env | xargs)

docker build -t prophetable . && docker run --rm \
    -v $VOLUME:/data \
    --env-file .env \
    --name=pm \
    prophetable