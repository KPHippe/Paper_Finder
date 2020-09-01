import os
import sys
import json
import argparse
from os.path import isfile

CONFIG_PATH = './.config/'

def setup_email():
    '''
    This is the setup routine for the email part of the script
    The end goal of this method is to establish a JSON file for the email to use.

    Requirements:
    ---------------
    - GMail account with low security apps access and a python password (directions in README)
    - list of recipients

    '''
    print('Email setup, fields to setup: sender email, sender password, reciepeints list')
    if isfile(f"{CONFIG_PATH}email_config.json"):
        delete = input("\nWe detect an email config present, would you like to delete the config and restart from scrath? [y/n]\n>>>")
        if 'y' in delete or 'Y' in delete:
            os.system('rm -f ./.config/email_config.json')
        else:
            print('Current config saved, setup in append mode')

    email_config = {"sender_email": None,
                    "sender_password": None,
                    "recipients": []}
    if isfile(f"{CONFIG_PATH}email_config.json"):
        email_config = json.load(open(f"{CONFIG_PATH}email_config.json"))

    action = input('Action (choices: -r add to recipeints list, -s: update sender email, -p: update sender password, quit/QUIT to exit email setup)\n>>>')
    while not ('QUIT' in action or 'quit' in action):
        if '-r' in action:
            cur_recipients = email_config['recipients']
            print(f'Current recipeints: {cur_recipients}')
            r_action = input('Delete: -d user@domain.com\nAdd: -a user@domain.com\nQuit: -f\n\n>>>')
            while '-f' not in r_action:
                if '-d' in r_action:
                    delete_email = r_action.split('-d')[-1].strip()
                    print(f"Deleting: {delete_email}\n\n")

                    try:
                        del email_config['recipients'][cur_recipients.index(delete_email)]
                    except:
                        print(f"Deleting '{delete_email}' failed...")

                    cur_recipients = email_config['recipients']
                    print(f'Current recipeints: {cur_recipients}\n')

                if 'a' in r_action:
                    add_email =  r_action.split('-a')[-1].strip()
                    print(f'Adding: {add_email}')

                    email_config['recipients'].append(add_email)
                    cur_recipients = email_config['recipients']
                    print(f'Current recipeints: {cur_recipients}\n')

                r_action =input('Recipients actions:\nDelete: -d user@domain.com\nAdd: -a user@domain.com\nFinished editing recipients: -f\n>>>')

        elif '-s' in action:
            add_email = input('Sender email (e.g. Paper_Finder@gmail.com)\n>>>')
            email_config['sender_email'] = add_email.strip()
            sender_email = email_config['sender_email']
            print(f"Sender email: {sender_email}\n\n")

        elif '-p' in action:
            new_password = input('Sender email password (e.g. password123)\n>>>')
            email_config['sender_password'] = new_password

            print(f"Updated password...\n\n")

        else:
            print(f"Unknown action '{action}'")

        action = input('\nAction (choices: -r add to recipeints list, -s: update sender email, -p: update sender password, quit/QUIT to exit email setup)\n>>>')



    #Dump and change permissions that only the owner can read and write
    json.dump(email_config, open(f"{CONFIG_PATH}email_config.json", 'w'))
    os.system(f'chmod 600 {CONFIG_PATH}email_config.json')

    print('Email configuration set')

def setup_scraper():
    '''
    This portion of the setup creates the JSON file that allows the scraper
    to filter articles based on keywords.

    Result is a private json file that are the basis for filtering articles in ArXiv
    I will be adding more sites soon
    
    '''
    print('Scraper setup, fields to setup: ArXiv keywords, as more sites get added, more fields will be present')
    if isfile(f"{CONFIG_PATH}scraper_config.json"):
        delete = input("We detect an scraper config present, would you like to delete the config and restart from scrath? [y/n]\n>>>")
        if 'y' in delete or 'Y' in delete:
            os.system('rm -f ./.config/scraper_config.json')
        else:
            print('Current config saved, setup in append mode')

    scraper_config = {"ArXiv": []}
    if isfile(f"{CONFIG_PATH}scraper_config.json"):
        scraper_config = json.load(open(f"{CONFIG_PATH}scraper_config.json"))

    cur_keywords = scraper_config['ArXiv']
    print(f"Current keywords: {cur_keywords}")

    action = input('\nAction (choices: -a add to keywords list, -d: delete keyword from list, quit/QUIT to exit email setup)\n>>>')
    while not ('QUIT' in action or 'quit' in action):
        if '-a' in action:
            keyword = input("Keyword/phrase: ")
            scraper_config['ArXiv'].append(keyword.strip())

            cur_keywords = scraper_config['ArXiv']
            print(f'New keywords: {cur_keywords}')
        elif 'd' in action:
            delete_word = input("Word/phrase to delete: ")

            try:
                del scraper_config['ArXiv'][cur_keywords.index(delete_word)]
            except:
                print(f"Deleting '{delete_word}' failed...")

            cur_keywords = scraper_config['ArXiv']
            print(f'New keywords: {cur_keywords}')

        else:
            print(f"Action: {action} not recognized")

        action = input('\nAction (choices: -a add to keywords list, -d: delete keyword from list, quit/QUIT to exit email setup)\n>>>')


    json.dump(scraper_config, open(f"{CONFIG_PATH}scraper_config.json", 'w'))
    os.system(f'chmod 600 {CONFIG_PATH}scraper_config.json')

    print('Scraper configuration set')


def create_folder(pathToFolder):
    try:
        os.mkdir(pathToFolder)
    except FileExistsError:
        print(f"'{pathToFolder}' already exists...")
    except Exception as e:
        print(f"Fatal error creating: '{pathToFolder}'...")
        print(f'Exception: {e}')
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Run configurations for Paper_Finder')
    parser.add_argument('-e','--email', action='store_true', help='Run the setup for the email part of Paper_Finder, fields applicable: sender email, sender password, recipeints list')
    parser.add_argument('-s', '--scraper', action='store_true', help='Run the setup for the scraping part of Paper_Finder, fields applicable:\n\tkeywords')
    #TODO: figure out what a default parameter set would look like
    # parser.add_argument('-d', '--default', help='Will set up Paper_Finder with default parameters, no email functionality will be added')

    args = parser.parse_args()

    create_folder(CONFIG_PATH)

    if args.email:
        print('Configuring email...\n\n\n')
        setup_email()
    if args.scraper:
        print('Configuring scraper...\n\n\n')
        setup_scraper()

    print('\nAll configuration complete!\nRun Paper_Finder with the command: python Paper_Finder.py')
