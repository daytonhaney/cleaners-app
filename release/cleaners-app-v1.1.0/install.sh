#!/bin/bash
# Cleaners App Installation Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Cleaners App Installation Script${NC}"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "demo.py" ]; then
    echo -e "${RED}Error: Please run this script from the cleaners-app directory${NC}"
    exit 1
fi

# Check if executables exist
if [ ! -d "dist" ] || [ ! -f "dist/cleaners-app" ] || [ ! -f "dist/cleaners-demo" ]; then
    echo -e "${YELLOW}Building executables...${NC}"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Activate and build
    source venv/bin/activate
    pip install -r requirements.txt faker
    pyinstaller --onefile --name cleaners-app main.py
    pyinstaller --onefile --name cleaners-demo demo.py
    deactivate
    
    echo -e "${GREEN}Build completed!${NC}"
else
    echo -e "${GREEN}Executables already built.${NC}"
fi

echo ""
echo -e "${GREEN}Installation Complete!${NC}"
echo "============================"
echo ""
echo "Available Commands:"
echo -e "${YELLOW}  ./dist/cleaners-app${NC}     - Run production app"
echo -e "${YELLOW}  ./dist/cleaners-demo${NC}    - Run demo with fake data"
echo ""
echo "CLI Options:"
echo -e "${YELLOW}  --help${NC}                      Show help"
echo -e "${YELLOW}  --version${NC}                   Show version"
echo -e "${YELLOW}  --license${NC}                   Show license"
echo -e "${YELLOW}  --man${NC}                        Show manual page"
echo ""
echo "Demo-specific Options:"
echo -e "${YELLOW}  --generate-data [COUNT]${NC}       Generate fake data"
echo -e "${YELLOW}  --demo-stats${NC}                 Show database statistics"
echo ""
echo "Examples:"
echo -e "${YELLOW}  ./dist/cleaners-app --help${NC}"
echo -e "${YELLOW}  ./dist/cleaners-demo --generate-data 10${NC}"
echo -e "${YELLOW}  ./dist/cleaners-demo --demo-stats${NC}"
echo ""
echo -e "${GREEN}Enjoy using Cleaners App!${NC}"