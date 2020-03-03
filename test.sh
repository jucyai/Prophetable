export $(egrep -v '^#' .env | xargs)

docker build -t prophetmodeller . && docker run --rm \
    -v $VOLUME:/data \
    --name=pm \
    prophetmodeller