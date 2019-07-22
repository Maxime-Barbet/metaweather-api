#!/bin/sh

BASEDIR=$(cd "$(dirname "${0}")"; pwd)

echo 'Activate virtualenv'
. "${BASEDIR}/venv/bin/activate"

echo 'Run Metaweather'
metaweather $1