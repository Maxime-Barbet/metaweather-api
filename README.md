# Metaweather API

## Requirements

Install a docker.

## Setup

Build your docker image with the command `docker build --tag metaweather`in the root directory.

## Usage
```
# use a variable to fix issue on location with compound noun.
location="Los Angeles"
docker run metaweather $location
```

## Tests

Run the test in using pytest library with the command `pytest`.