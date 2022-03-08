#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\e[34m'
YELLOW='\033[1;33m'
PURPLE='\033[1;35m'
NC='\033[0m'
CLEAR_LINE='\r\033[K'
UP='\033[1A'
BOLD='\e[1m'
NORMAL='\e[21m'


# Exit if any subcommand fails
#set -e

# file system creation
function filesys {
    DIR=/Users/`whoami`/Desktop/cs10_test/unit_00
    if [ ! -d "$DIR" ]; then
        mkdir -p $DIR

    fi
}

function setup_venv {
    # Setting up virtual environment
    printf "${CLEAR_LINE}🗂  ${BLUE}Creating virtual environment...${NC}\n"
    
    if [[ $SHELL == *"bash" ]];
    then
        FILE=/Users/`whoami`/.bashrc
        if [ ! -e $FILE ]; then
            printf 'eval "$(direnv hook bash)"' > $FILE
        else
            if ! grep -q 'eval "$(direnv hook bash)"' "$FILE"; then
                cp $FILE ${FILE}_pre_cs10
                printf '\n# Added for ISF cs10 setup.\n# Original bash profile can be found in .bash_profile_pre_cs10\neval "$(direnv hook bash)"' >> $FILE
            fi
        fi
        source ~/.bashrc
    elif [[ $SHELL == *"zsh" ]];
    then
        FILE=/Users/`whoami`/.zshrc
        if [ ! -e $FILE ]; then
            printf 'eval "$(direnv hook zsh)"' > $FILE
        else
            if ! grep -q 'eval "$(direnv hook zsh)"' "$FILE"; then
                cp $FILE ${FILE}_pre_cs10
                printf '\n# Added for ISF cs9 setup.\n# Original zsh profile can be found in .zshrc_pre_cs9\neval "$(direnv hook zsh)"' >> $FILE
            fi
        fi
        source ~/.zshrc
    else
        printf "Sorry, $SHELL is not supported. Please switch to bash or zsh and try again."
    fi
    DIR=~/Desktop/cs10_test/
    cd $DIR
    printf 'PATH_add env/bin\n' >> .envrc
    python3 -m venv env
    direnv allow .
}

printf "┌── 👋\n"
printf "│   ${PURPLE}Welcome to the CS10 setup script! Running this script will set up your new directory.${NC}\n"
printf "│   ${PURPLE}Note: the setup may ask for your password. As a security measure, you${NC}\n"
printf "│   ${PURPLE}won't see any characters when you type it in.${NC}\n"
read -p "│   Ready to begin? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
printf "\n"

printf "🗂  ${BLUE}Setting up cs10 folder on Desktop...${NC}\n"
filesys
setup_venv
printf "${CLEAR_LINE}👍  ${GREEN}cs10 folder created!${NC}\n"

printf "${PURPLE}Your computer is configured! Please restart Terminal. ${NC}\n"
exit 0
