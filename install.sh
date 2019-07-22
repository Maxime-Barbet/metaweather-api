#!/bin/sh

BASEDIR=$(cd "$(dirname "${0}")"; pwd)

pip3 install virtualenv

echo 'Create virtualenv repository'
virtualenv "${BASEDIR}/venv"

echo 'Activate virtualenv'
. "${BASEDIR}/venv/bin/activate"

echo 'Install metaweather package'
pip3 install --editable "${BASEDIR}"
