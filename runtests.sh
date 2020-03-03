#!/usr/bin/env bash 

OPTS="$@"

clear; reset;

./manage.py test --failfast $OPTS tests

