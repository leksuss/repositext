#!/usr/bin/env bash

OPTS="$@"
PYTHON=$(which python)

source getenv.sh

source getenv.sh

OPTS=$(local_settings)

function display_head() {
	echo "Running Django Development Server with following:"
	echo "-------------------------------------------------"
	$PYTHON -VV
	echo "Using: $(pyenv virtualenv-prefix)"
	echo "Environment: $(pyenv local)"
	echo "Which: $(pyenv which $PYTHON)"
	echo "Source: $(pyenv version-file)"
}

function start_server() {
	$PYTHON manage.py runserver $OPTS
}


function main() {
	# clear; reset;
	display_head
	start_server
}

main
