#!/bin/bash
# Cleaning Service Manual Backup & Recovery Script
# 
# This script provides manual backup/recovery operations separate from the app's built-in backup
# Use for administrative purposes, cron jobs, or when app is not running
#
function backup_database(){
    
    # various techniques exists to backup/ recover - learning purposes only

    DESTINATION_DIR="$HOME/database-backups"
    DB_NAME="business_data.db"
    
    if [ ! -f "$DB_NAME" ]; then
        echo "Database file $DB_NAME not found!"
        return 1
    fi
    
    BACKUP_NAME="business_data_backup-$(date +%Y-%m-%d).db"
    
    mkdir -p "$DESTINATION_DIR"
    sqlite3 "$DB_NAME" ".backup '$DESTINATION_DIR/$BACKUP_NAME'"
    echo "Backup successful: $BACKUP_NAME in $DESTINATION_DIR"
    
    gzip -f "$DESTINATION_DIR/$BACKUP_NAME"
    echo "Backup compressed: $BACKUP_NAME.gz"
    echo "Copy and archive of database successful"

}

backup_database

function recover_database(){
    
    BACKUP_DIR="$HOME/database-backups"
    
    if [ ! -d "$BACKUP_DIR" ]; then
        echo "Backup directory not found: $BACKUP_DIR"
        return 1
    fi
    
    # Get list of available backups
    BACKUP_LIST=$(ls -la "$BACKUP_DIR" | grep ".gz" | awk '{print $9}' | sed 's/business_data_backup-//' | sed 's/.db.gz//' | sort -r)
    
    if [ -z "$BACKUP_LIST" ]; then
        echo "No backup files found in $BACKUP_DIR"
        return 1
    fi
    
    # Create a simple "popup" box using only built-in tools
    clear
    echo "=================================================================="
    echo "                  DATABASE RECOVERY TOOL                   "
    echo "=================================================================="
    echo ""
    echo "Available Backups:"
    echo ""
    
    # Display backups in a numbered list with file info
    i=1
    for backup in $BACKUP_LIST; do
        file_size=$(ls -lh "$BACKUP_DIR/business_data_backup-$backup.db.gz" | awk '{print $5}')
        echo "  [$i] $backup (Size: $file_size)"
        i=$((i + 1))
    done
    
    echo ""
    echo "=================================================================="
    echo "Enter backup number to restore (0 to cancel): "
    read -r SELECTION
    
    if [ "$SELECTION" = "0" ]; then
        echo "Restore cancelled"
        return 0
    fi
    
    # Get the selected backup date
    i=1
    SELECTED_BACKUP=""
    for backup in $BACKUP_LIST; do
        if [ "$i" -eq "$SELECTION" ]; then
            SELECTED_BACKUP="$backup"
            break
        fi
        i=$((i + 1))
    done
    
    if [ -z "$SELECTED_BACKUP" ]; then
        echo "Invalid selection!"
        return 1
    fi
    
    BACKUP_FILE="$BACKUP_DIR/business_data_backup-$SELECTED_BACKUP.db.gz"
    
    # Confirmation "popup"
    echo ""
    echo "=================================================================="
    echo "                       CONFIRM RESTORE                            "
    echo "=================================================================="
    echo ""
    echo "You are about to restore from backup dated: $SELECTED_BACKUP"
    echo ""
    echo "WARNING: This will REPLACE the current database file!"
    echo ""
    echo "Type 'yes' to confirm restore, or anything else to cancel: "
    read -r CONFIRM
    
    if [ "$CONFIRM" = "yes" ]; then
        gunzip -c "$BACKUP_FILE" > business_data.db
        echo ""
        echo "=================================================================="
        echo "                      RESTORE COMPLETE                            "
        echo "=================================================================="
        echo "Database successfully restored from backup dated $SELECTED_BACKUP"
        echo "Current database size: $(ls -lh business_data.db | awk '{print $5}')"
    else
        echo "Restore cancelled by user"
    fi

}



function source_backups(){

    echo "Available backups in $DESTINATION_DIR:"
    ls -la "$HOME/database-backups/" | grep ".gz"

}



# Uncomment to use these functions:
# backup_database  # Run backup immediately
# source_backups   # List available backups  
# recover_database # Restore from backup
