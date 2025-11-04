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
import time


# CLI packages
import argparse


# Web Dashboard
from web import index as webapp


# exploits module
from exploit_modules.exploits import Exploits


# import yung lightweight DB natin
from database.db_init import init_db

def cli_banner():

    banner = print(r""" 

                                 ______
                              .-"      "-.
                             /            \
                            |              |
                            |,  .-.  .-.  ,|
                              )(_o/  \o_)(       OPERATION : WEBSPEAR        
                             /     /\     \      AUTHOR : 0slo
                  (@_       (_     ^^     _)
            _     ) \_______\__|IIIIII|__/__________________________
            (_)@8@8{}<________|-\IIIIII/-|___________________________>
                    )_/       \          /
                    (@         `--------`

    
    """)

    return banner










def main():
    init_db()

    parser = argparse.ArgumentParser(description="WebSpear: Automated Web Recon and Exploitation Framework")
    parser.add_argument('-s', '--scan', help="Target URL to scan", type=str)

    parser.add_argument('-d', '--dashboard', help="Enable Dashboard UI", action="store_true")
    parser.add_argument('-c', '--cli', help="Run in CLI mode (no dashboard)", action="store_true")

    parser.add_argument('--all', help="Enable all exploit modules", action="store_true")
    parser.add_argument('--xss', help="Enable XSS scanner", action="store_true")
    parser.add_argument('--sqli', help="Enable SQL injection scanner", action="store_true")
    parser.add_argument('--lfi', help="Enable LFI/RFI/path traversal detection", action="store_true")
    parser.add_argument('--js', help="Enable JavaScript endpoint inspection", action="store_true")
    parser.add_argument('--ddos', help="Enable basic DoS fuzzing", action="store_true")
    parser.add_argument('--brute', help="Enable login bruteforce via Playwright", action="store_true")

    args = parser.parse_args()

    if not args.scan:
        print(colored("[!] Error: target URL not provided", "red"))
        print("🧠 Tip: use -h to display available options")
        exit()

    target_url = args.scan
    exploits = Exploits(target_url)

    if args.dashboard:
        print(colored(f"[+] Starting dashboard for target: {target_url}", "yellow"))
        from web import run_flask_server 
        run_flask_server()
        return

    if args.cli:
        print(colored(f"[+] Running CLI scan for: {target_url}", "yellow"))
        cli_banner()
        
        if args.all:
           exploits.start_exploit_engine()
        else:
            if args.xss:
                exploits.run_xss()
            if args.sqli:
                exploits.run_sqli()
            if args.lfi:
                exploits.run_lfi_rfi()
            if args.js:
                exploits.run_js_scraper()
            if args.ddos:
                exploits.run_ddos()
            if args.brute:
                exploits.run_playwright_login_bruteforce()
            else:
                print(colored("[-] You forgot to select attack module", "red"))
                exit()
                
        print(colored("[✓] Scan complete. Results saved to database.", "green"))
        return

    print(colored("[!] You must specify --cli or --dashboard", "red"))
    print("💡 Example: python main.py -s https://target.com --cli --all")
    exit()



if __name__ == "__main__":
    main()