export $(egrep -v '^#' .env | xargs)

docker build -t prophetmodeller . && docker run --rm \
    -v $VOLUME:/app/data \
    --name=pm \
    prophetmodeller