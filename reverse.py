#!/usr/bin/env python3
# file: reverse.py
# Reverse Whois Search
# Version: v0.1

import requests
import sys
import json
import argparse
from config import api_url,api_key
from pyfiglet import figlet_format

def banner():
    print(figlet_format("Reverse Whois"))
    print("Horizontal Domain Enumeration")
    print("Github: @kbehroz")
    print("Twitter: @behroznathwani\n\n")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Name of Organization", nargs='+', required=True)
    parser.add_argument("-o", "--output", help="Output File name")
    return parser.parse_args()

def parse(api_key,org):
    try:
        response = requests.get(F"https://user.whoisxmlapi.com/service/account-balance?apiKey={api_key}").json()
        if 'data' not in response: # Validating Api Key
            print("Invaild Api Key. Please set correct API Key in config.py")

        elif response['data'][3]['credits'] < 0: # Checking credits
            print("You don't have API call credits")
        else:
            domainlist(org)
    except requests.exceptions.RequestException as e:
        print(e)


def domainlist(org):
    payload = {
    'apiKey': api_key,
    'searchType': 'current',
    'mode': 'preview',
    'basicSearchTerms':{
                'include': [
                org
                ]
              }
    }

    try:
        print("[+] Trying to Fetch Domains")
        content = requests.post(api_url, json=payload).json()
        if content['domainsCount'] > 0:
            print(f"[+] {content['domainsCount']} domain Found.")
            output_domain(payload,org)
        else:
            print("[+] No domain found")
    except requests.exceptions.RequestException as e:
        print(e)

def output_domain(post_data,org):
    post_data['mode'] = 'purchase'
    try:
        domains = requests.post(api_url, json=post_data).json()
        for domain in domains['domainsList']:
            print(domain)
            if parse_args().output:
                with open(parse_args().output,"a") as file:
                    file.write(domain)
                    file.write("\n")

    except requests.exceptions.RequestException as e:
        print(e)


def main():
    banner()
    org = ' '.join(parse_args().target)
    parse(api_key,org)

try:
    main()
except KeyboardInterrupt:
    print('Keyboard Interruption....')
    sys.exit(0)

