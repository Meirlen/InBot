


def set_endpoints(action_url):
    path = './endpoints.yml'
    f = open(path, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(path, 'w')
    is_start = False
    for line in linelist:
        if line.strip() == '# End':
           is_start = False  
        if is_start:
           key_name,value_config = line.split(': "')
           if key_name.strip() == 'url':
              line = '  url: "' + action_url+'" \n'
        #    line = line.replace('Miko', 'new')
        if line.strip() == 'action_endpoint:':
            is_start = True
        f2.write(line)

    f2.close()

def set_credentials(token,bot_name,webhook_url):
    path = './credentials.yml'
    f = open(path, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(path, 'w')
    is_start = False
    for line in linelist:
       
       
        if line.strip() == '# End':
           is_start = False  
        if is_start:
           key_name,value_config = line.split(': "')
           print(key_name)
           
           if key_name.strip() == 'access_token':
              line = '  access_token: "' + token+'" \n'
           if key_name.strip() == 'verify':
              line = '  verify: "' + bot_name+'" \n'
           if key_name.strip() == 'webhook_url':
              line = '  webhook_url: "' + webhook_url+'" \n'


              print(line)
        #    line = line.replace('Miko', 'new')
        if line.strip() == 'custom_telegram.TelegramInput:':
            is_start = True


        f2.write(line)

    f2.close()


def set_constans(is_release,action_endpoint):
    path = '/Users/meirlen/Desktop/bot/y/actions/app_constans.py'
    f = open(path, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(path, 'w')
    is_start = False
    counter = 0
    for line in linelist:
        counter+=1
        if counter == 6:
            if is_release:
              line = 'TELEGRAM_IS_PROD = True \n'  
            else:
              line = 'TELEGRAM_IS_PROD = False \n'  
        if counter == 8:
            if is_release:
              line = 'ACTION_ENDPOINT = "http://localhost:5006" \n'  
            else:
              line = 'ACTION_ENDPOINT = "http://localhost:5005" \n'   
            # line = 'ACTION_ENDPOINT = "'+action_endpoint+'"\n'  
         
            print(line) 
        f2.write(line)

    f2.close()



def change_build_mode(is_release):
    if is_release:
        # Prod
        webhook = "https://rasa-server-meirlen.cloud.okteto.net/webhooks/telegram/webhook"
        action_endpoint = "http://rasa-actions-server:5055/webhook"

    
        set_credentials("5350351478:AAGxTzWfuEBBmhKMxUin76kStfZSaE2Gny0","kkk09bot",webhook)    
        set_endpoints(action_endpoint)
        # set_constans(is_release,action_endpoint)

    else:
        # Debug
        webhook = "https://3a99-37-99-122-186.ngrok.io/webhooks/telegram/webhook"
        action_endpoint = "http://localhost:5055/webhook"

        set_credentials("5193584451:AAGth9M7cE5YteQW01Nb8h4ioGh-HT_9SjQ","MeirlenBot", webhook)    
        set_endpoints(action_endpoint)
        # set_constans(is_release,action_endpoint)






import subprocess
from trace import Trace
import requests


def generate_new_token():
    out = subprocess.Popen(['yc', 'iam', 'create-token'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    new_token = str(stdout)
    size = len(new_token)
    new_token = new_token[2:size-3]
    print(new_token)
    return new_token


def update_yandex_token_in_prod(new_token):
    url = 'https://rasa-server-meirlen.cloud.okteto.net/webhooks/rest/webhook'
    response = requests.post(
            url = url,
            json={
                'sender': 'admin',
                'message': 'new token:'+new_token,
            }
        )


    print(response) 




# SETUP BUILD MODE 
# Prod: don't forget pull db from server
# # Bug: double call
change_build_mode(is_release = True)

# update_yandex_token_in_prod(generate_new_token())
# generate_new_token()
# generate_new_token()


# Make ngrok public api: ngrok http 5005

# digital ocean pass apA91ata!a
# Install Docker in do
# curl -fsSL https://get.docker.com -o get-docker.sh


# git commit -m "Remove ignored files"
#  git config --global user.email "miko_982@mail.ru"
#  git config --global user.name "Meirlen"

# git remote add origin https://github.com/Meirlen/InBot.git
# git remote set-url origin https://github.com/Meirlen/InBot.git

# git branch -M main
# git push -u origin main

# git push origin master


# cmd
# rm -rf directory_name
# docker container ls
# docker rm 5c7a2a2632b8
# docker stop 5c7a2a2632b8
# docker-compose up
