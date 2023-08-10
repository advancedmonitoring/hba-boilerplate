red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
blue=$(tput setaf 4)
am=$(tput setaf 208)
reset=$(tput sgr0)

PROJECT=${1:-project}
PYTHON_VERSION="3.10"
VENV_NAME="ENV"
HUMAN_PROJECT_NAME=$(sed "s/_/ /g" <<<"$PROJECT")
HUMAN_PROJECT_NAME_CAPITALIZED=${HUMAN_PROJECT_NAME^}

echo $am
cat docs/logo_ascii.txt | sed -e "s/{YELLOW}/${yellow}/g" \
-e "s/{BLUE}/${blue}/g" \
-e "s/{RESET}/${am}/g" \
-e "s/{PROJECT_SLUG}/${PROJECT}/" \
-e "s/{PROJECT_NAME}/${HUMAN_PROJECT_NAME_CAPITALIZED}/" \
-e "s/{PYTHON_VERSION}/${PYTHON_VERSION}/" \
-e "s/{VENV_NAME}/${VENV_NAME}/"
echo $reset

update_project_files() {
  echo "${blue}Update config files...${reset}"
  find backend/config/ -type f -name "*.*" | xargs sed -i "s/{PROJECT_NAME}/${PROJECT}/g"
  find backend/config/ -type f -name "*.*" | xargs sed -i "s/{HUMAN_PROJECT_NAME_CAPITALIZED}/${HUMAN_PROJECT_NAME_CAPITALIZED}/g"
  echo "${green}Config files updated!${reset}"
  sleep 1

  echo "${blue}Create local settings file...${reset}"
  mv backend/config/settings/_local.py backend/config/settings/local.py
  echo "${green}Local settings file created!${reset}"
  sleep 1

  echo "${blue}Update locale files...${reset}"
  find backend/locale/ -type f -name "*.*" | xargs sed -i "s/{PROJECT_NAME}/${PROJECT}/g"
  echo "${green}Locale files updated!${reset}"
  sleep 1

  echo "${blue}Update project files...${reset}"
  find backend/project/ -type f -name "*.*" | xargs sed -i "s/{PROJECT_NAME}/${PROJECT}/g"
  find frontend/ -type f -name "*.*" | xargs sed -i "s/{PROJECT_NAME}/${PROJECT}/g"
  echo "${green}Locale files updated!${reset}"
  sleep 1

  echo "${blue}Update template files...${reset}"
  find backend/templates/ -type f -name "*.*" | xargs sed -i "s/{PROJECT_NAME}/${PROJECT}/g"
  find backend/templates/ -type f -name "*.*" | xargs sed -i "s/{HUMAN_PROJECT_NAME_CAPITALIZED}/${HUMAN_PROJECT_NAME_CAPITALIZED}/g"
  echo "${green}Template files updated!${reset}"
  sleep 1

  echo "${blue}Update gitignore file...${reset}"
  sed -i "s/{PROJECT_NAME}/${PROJECT}/g" .gitignore
  echo "${green}Gitignore file updated!${reset}"
  sleep 1

  echo "${blue}Rename project apps directory...${reset}"
  mv ./backend/project ./backend/${PROJECT}
  echo "${blue}Project apps directory rename done!${reset}"
  sleep 1
}

create_virtualenv() {
  echo "${blue}Creating virtualenv...${reset}"
  python${PYTHON_VERSION} -m venv ${VENV_NAME}
  echo "${green}Virtualenv \"${VENV_NAME}\" was created${reset}"
  sleep 2
}

activate_virtualenv() {
  echo "${blue}Activate virtualenv...${reset}"
  source ${VENV_NAME}/bin/activate
  echo "${green}Virtualenv activated!${reset}"
  PS1="($(basename \"$VIRTUAL_ENV\"))\e[1;34m:/\W\e[00m$ "
  sleep 2
}

install_dependencies() {
  pip install -U pip
  pip install -r backend/requirements/local.txt
}

print_tutorial() {
  echo "$blue Next steps:$reset"
  echo "    Activate virtual environment    ${green}source ${VENV_NAME}/bin/activate${reset}"
  echo ""
  echo "$blue Run server with:$reset"
  echo "    Go to backend code dir          ${green}cd backend${reset}"
  echo "    Apply DB migrations             ${green}python manage.py migrate${reset}"
  echo "    Create superuser                ${green}python manage.py createsuperuser${reset}"
  echo "    Run developer server            ${green}python manage.py runserver${reset}"
  echo ""
  echo "$blue Run frontend server in new terminal with:$reset"
  echo "    Go to frontend code dir          ${green}cd frontend${reset}"
  echo "    Install dependencies             ${green}npm i${reset}"
  echo "    Run frontend server              ${green}npm run serve${reset}"
  echo ""
  echo "$blue Start code your awesome project!$reset"
  echo "    Go to rtd to start              https://readthedocs.org/"
}

remove_setup() {
  rm setup.sh
}

update_project_files
create_virtualenv
activate_virtualenv
install_dependencies
print_tutorial
remove_setup
