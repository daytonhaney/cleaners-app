#!/bin/bash

function backup_database(){
    
    # various techniques exists to backup/ recover - learning purposes only

    DESTINATION_DIR="$HOME/database-backups"
    DB_NAME="business_data.db"
    BACKUP_NAME="business_data_backup-$(date +%Y-%m-%d).db"
    
    mkdir -p "$DESTINATION_DIR"
    sqlite3 "$DB_NAME" ".backup '$DESTINATION_DIR/$BACKUP_NAME'"
    echo "Backup successful: $BACKUP_NAME in $DESTINATION_DIR"
    
    gzip -f "$DESTINATION_DIR/$BACKUP_NAME"
    echo "Backup compressed: $BACKUP_NAME.gz"
    echo "Copy and archive of the database successful"

}

backup_database

function recover_database(){
    
    gunzip business_data_backup-2024-02-14.db.gz
    sqlite3 .attach 'business_data_backup-2024-02-14.db' as restored;
}


#recover_database
