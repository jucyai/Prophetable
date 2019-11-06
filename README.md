# Docker Prophet Modeller

## Build

```sh
docker build -t prophetmodeller .

# Clean rebuild
# docker build --no-cache -t prophetmodeller .
```

## Run

```sh
docker run --rm -it -d \
    -v /path/to/volume/data:/app/data \
    --name=pm \
    prophetmodeller \
    bash run.sh
```

## Log

```sh
docker logs pm
```

## Stop

```sh
docker stop pm
```

## Cleanup

```sh
docker rm pm
```
