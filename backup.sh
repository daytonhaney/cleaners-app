#!/bin/bash

function backup_database(){

    DESTINATION_DIR="$HOME/database-backups"
    DB_NAME="business_data.db"

    cp business_data.db busisness_data_backup.db
    
    BACKUP_NAME="backup-"$(date +%Y-%m-%d)"".gz
    mkdir -p "$DESTINATION_DIR"
    sqlite3 "$DB_PATH" .dump | gzip > "$DESTINATION_DIR/$BACKUP_NAME"
    echo "Backup successful: $BACKUP_NAME in $DESTINATION_DIR"
    
    mv busisness_data_backup.db $DESTINATION_DIR
    # recover the gzip 
    gzip -d $DESTINATION_DIR/$BACKUP_NAME
    echo "copy and archive of database successful"
}

backup_database
 
