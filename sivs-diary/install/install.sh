#!/bin/bash

DOINSTALL=true

#Copy env
mv ../.env.template ../.env

# Check if user is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Check if the ubuntu user exists; if not, create the user
if ! id -u ubuntu >/dev/null 2>&1; then
    sudo useradd -m -s /bin/bash ubuntu
    echo "User 'ubuntu' created."
else
    echo "User 'ubuntu' already exists."
fi

# Add the ubuntu user to the sudo group
sudo usermod -aG sudo ubuntu
echo "User 'ubuntu' added to sudo group."

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if [ $DOINSTALL  == true ]; then
  # Install Apache
  echo "Installing Apache..."
  sudo apt-get update
  sudo apt-get  install -yq apache2
  sudo a2enmod headers
  sudo a2enmod proxy
  sudo a2enmod proxy_http
  sudo cp -f ./services/envvars /etc/apache2/

  # Install Python3
  echo "Installing Python3..."
  sudo apt-get -yq install python3-full
  sudo python3 -m venv /home/ubuntu/venv
  source  /home/ubuntu/venv/bin/activate
  pip install -r requirements.txt
  deactivate
  #Install
  echo "Installing Docker..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh ./get-docker.sh
  sudo apt-get install -yq docker-compose-plugin
  sudo apt-get install -yq docker-compose

fi

#Configure Firewall
echo "Configuring Firewall..."
sudo ufw allow ssh
sudo ufw disable
echo "Script executed."


#Start Docker
sudo docker-compose up -d

#Populate Database
echo "Waiting for 20 seconds..."
sleep 20
echo "Populating Database"
source  /home/ubuntu/venv/bin/activate
python3 create_db.py
deactivate

#Copy frontend to /var/www/html
echo "Copying sivs-diary.tar to /var/www/html"
sudo cp  ../../sivs-diary.tar.xz /var/www/html/
sudo cp prepare.sh /var/www/html/

#Remove Diary Installation
systemctl stop sivs-diary_service
systemctl disable sivs-diary_service
rm /usr/local/bin/sivs-diary_service.sh
rm /etc/systemd/system/sivs-diary_service.service
systemctl daemon-reload
systemctl reset-failed

#Install Diary Service
sudo cp -r ./services/sivs-diary_service.sh /usr/local/bin
sudo chmod +x /usr/local/bin/sivs-diary_service.sh
sudo cp -r ./services/sivs-diary_service.service /etc/systemd/system/

#Start Diary Service
sudo systemctl daemon-reload
sudo systemctl enable sivs-diary_service
sudo service sivs-diary_service start

#Disable all Sites Apache
cd /etc/apache2/sites-available/
sudo a2dissite *
sudo service apache2 restart
cd $DIR

#Copy Files to Apache
sudo cp -r ./services/file-server.conf /etc/apache2/sites-available/
sudo a2ensite file-server.conf
sudo cp -r ./services/sivs-diary.conf /etc/apache2/sites-available/
sudo a2ensite sivs-diary.conf
sudo service apache2 restart