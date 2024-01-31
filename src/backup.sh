#!/bin/bash

function backup_database(){

    DB_PATH="database.db"
    BACKUP_NAME="backup-$(date +%Y-%m-%d)".sql.gz
    sqlite3 $DB_PATH .dump > $BACKUP_NAME | gzip "$BACKUP_NAME"
    echo "success: $BACKUP_NAME"

}

backup_database
