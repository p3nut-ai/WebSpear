'''
WebSpear

web pentesting automation from recon to exploit to reporting

author : 0slo

Todos:
    - Cli functions [done]
    - Web dashboard [done]
    - Exploit Automation
    - Saving data 
    - generating report


'''

from termcolor import colored


# CLI packages
import argparse


# Web Dashboard
from web import index as webapp


# exploits module
from exploit_modules.exploits import Exploits


# import yung lightweight DB natin
from database.db_init import init_db

def main():
    init_db()
    # webapp.run_flask_server()

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--scan', help="Set the target URL for victim" , type=str)
    parser.add_argument('-d', '--dashboard', help="enable dashboard UI", action="store_true")
    parser.add_argument('-c', '--cli', help="enable CLI no web dashboard", action="store_true")
    args = parser.parse_args()

    # check if nag provide ng url

    if args.scan is None:
        print(colored("[!] Error: target url not provided [!] \n", "red"))
        print("use -h to display help")
        exit()
 
    # Working on this first
    elif args.scan and args.dashboard is not None:

        '''
            FLOW

            get target
            call exploits
            run the crawler
            get the HTML code 
            analyze HTML code
            get the internal links
            form endpoints
            js files
            run exploits (IDOR, SSRF, XSS, SQLi, DDOS)
            generate report based on the findings
        '''


        print("runing dashboard with URL target")   
        
        target_url = args.scan

        exploits = Exploits(target_url)

        exploits.start_hunting()
        print("Running Flask now")
        webapp.run_flask_server()

    elif args.scan and args.dashboard is not None:
        print("runing CLI only with URL target")   


    else:
        print("Error running WebSpear use -h for help")
        exit()




# Run tong function if nirun yung main.py direcly 
if __name__ == "__main__":
    main()