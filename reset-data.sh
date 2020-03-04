#!/usr/bin/env bash

OPTS="$@"

source getenv.sh

OPTS=$(local_settings)

clear; reset;
./delete-pyc.sh

PYTHON=$(which python)
PROJ_INFO="$PYTHON project_info.py"
DB_INFO="$PROJ_INFO DATABASES default"

DBTYPE=$($DB_INFO ENGINE|cut -d"." -f4)
DBNAME=$($DB_INFO NAME)
DBUSER=$($DB_INFO USER)
DBPASS=$($DB_INFO PASSWORD)

MYSQL=$(which mysql)

MANAGE="${PYTHON} manage.py"

function reset_mysql() {
	echo "Working with MySQL ..."	
	DROP_DB_CMD="drop database ${DBNAME}"
	CREATE_DB_CMD="create database ${DBNAME}"

	echo "  Dropping database ${DBNAME} ..."
	${MYSQL} -u ${DBUSER} -p"${DBPASS}" -e "$DROP_DB_CMD"
	echo "   Done."
	echo "  Recreating database ${DBNAME} ..."
	${MYSQL} -u ${DBUSER} -p"${DBPASS}" -e "$CREATE_DB_CMD"
	echo "   Done."
}

function reset_postgresql() {
	echo "Working with Postgresql ..."
	DROP_DB_CMD="dropdb ${DBNAME}"
	CREATE_DB_CMD="createdb ${DBNAME} -O ${DBUSER}"

	echo "  Dropping database ${DBNAME} ..."
	$DROP_DB_CMD
	echo "   Done."
	echo "  Recreating database ${DBNAME} ..."
	$CREATE_DB_CMD
	echo "   Done."
}

function reset_sqlite3() {
	echo "Working with SQLite3 ..."
	DROP_DB_CMD="rm -rf db.sqlite3"
	CREATE_DB_CMD=""

	echo "  Dropping database ${DBNAME} ..."
	$DROP_DB_CMD
	echo "  Done."
	echo "  Migrations will create database automatically ..."
	echo "  Done."
}

function migrate() {

	rm -rf apps/repo/migrations

	${MANAGE} makemigrations $OPTS
	${MANAGE} migrate $OPTS
	${MANAGE} makemigrations repo $OPTS
	${MANAGE} migrate repo $OPTS
}

function create_superuser() {
	${MANAGE} createsuperuser --user admin --email admin@localhost --noinput $OPTS
}

function run_data_scripts() {
	$PYTHON scripts/data/folders.py
    $PYTHON scripts/data/documents.py
	$PYTHON scripts/data/users.py
    $PYTHON scripts/data/organizations.py
}

function main() {
	case $DBTYPE in
		mysql)
			reset_mysql;
			;;
		postgresql)
			reset_postgresql;
			;;
		sqlite3)
			reset_sqlite3;
			;;
			*)
			echo "A function for ${DBTYPE} has not been implemented."
			;;
	esac
	migrate
	create_superuser
	$PYTHON setadminpw.py
	run_data_scripts
}

main
