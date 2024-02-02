#!/bin/bash

function backup_database(){

    DESTINATION_DIR="$HOME/database-backups"
    DB_NAME="database.db"
    BACKUP_NAME="backup-$(date +%Y-%m-%d)".sql.gz
    mkdir -p "$DESTINATION_DIR"
    sqlite3 "$DB_PATH" .dump | gzip > "$DESTINATION_DIR/$BACKUP_NAME"
    echo "Backup successful: $BACKUP_NAME"
}

backup_database
 
