export $(egrep -v '^#' .env | xargs)

docker build -t prophetmodeller . && docker run --rm -it \
    -v $VOLUME:/app/data \
    --name=pm \
    prophetmodeller \
    bash run.sh