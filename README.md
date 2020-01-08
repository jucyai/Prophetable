# Docker Prophet Modeller

## Configure with prophet-config.json

TODO: Add support for all Prophet model parameters

```json
{
    "datafile": "example.csv",
    "traindatafile": "model_data.csv",
    "modeloutputfile": "output.csv",
    "modelpicklefile": "model.pickle",
    "holidaydatafile": "holidays_data.csv",
    "ds": "ds",
    "y": "y",
    "delimiter": ",",
    "floor": 0,
    "tsfreq": "D",
    "nafill": 0,
    "futureperiods": 10000,
    "mintraindate": "2012-08-01",
    "maxtraindate": "2014-07-31",
    "yearlyseasonality": true,
    "monthlyseasonality": false,
    "dailyseasonality": false,
    "holidays": [
        {
            "holiday": "h1",
            "ds": ["2016-11-25", "2017-11-24", "2018-11-23", "2019-11-28"],
            "lower_window": -5,
            "upper_window": 5
        },
        {
            "holiday": "h2",
            "ds": ["2017-07-10", "2018-07-17", "2019-07-14"],
            "lower_window": -5,
            "upper_window": 5
        }       
    ]
}
```

## Quick start

```sh
docker build -t prophetmodeller . && \
docker run --rm -it -d \
    -v /full/path/to/volume:/app/data \
    --name=pm \
    prophetmodeller \
    bash run.sh
```

## Build

```sh
docker build -t prophetmodeller .

# Clean rebuild
# docker build --no-cache -t prophetmodeller .
```

## Run

```sh
docker run --rm -it -d \
    -v /full/path/to/volume:/app/data \
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

## Caveats

- Must bind volume to `/app/data`
