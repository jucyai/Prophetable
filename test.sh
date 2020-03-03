export $(egrep -v '^#' .env | xargs)

docker build -t prophetable . && docker run --rm \
    -v $VOLUME:/data \
    --name=pm \
    prophetable