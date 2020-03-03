# Docker Prophet Modeller

## Quick start

```sh
docker build -t prophetmodeller . && \
docker run --rm -d \
    -v /full/path/to/volume:/data \
    --name=pm \
    prophetmodeller
```

## Build

```sh
docker build -t prophetmodeller .

# Clean rebuild
# docker build --no-cache -t prophetmodeller .
```

## Run

```sh
docker run --rm -d \
    -v /full/path/to/volume:/data \
    --name=pm \
    prophetmodeller
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
