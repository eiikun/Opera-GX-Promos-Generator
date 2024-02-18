import requests
import uuid
import time
import ctypes
import colorama
import random
import json
import sys
import os
import concurrent.futures

class Data:
    config = json.load(open('config.json', 'r')) ; success = 0 ; error = 0

    def getProxy():
        proxy = random.choice(open('Data/proxies.txt', 'r').read().splitlines())
        return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    
    #def clearTerminal():
    #    os.system("cls" if os.system == "nt" else "cls")

class Console:
    GREEN = "\033[38;5;120m" ; RED = "\033[38;5;9m" ; GRAY = "\033[38;5;238m"
    def success(text):
        print(f"{Console.GRAY}{time.strftime('%H:%M:%S')} {Console.GREEN}<+>{colorama.Fore.RESET} {text}")
    def error(text):
        print(f"{Console.GRAY}{time.strftime('%H:%M:%S')} {Console.RED}<->{colorama.Fore.RESET} {text}")

class Discord:
    def __init__(self) -> None:
        self.client = requests.Session()
        self.client.proxies = Data.getProxy() if Data.config['proxyless'] != True else None
        self.client.headers = {'authority': 'api.discord.gx.games', 'accept': '*/*', 'accept-language': 'en-US,en;q=0.9', 'content-type': 'application/json', 'origin': 'https://www.opera.com', 'referer': 'https://www.opera.com/', 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Opera GX";v="106"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'}
        self.url = "https://api.discord.gx.games/v1/direct-fulfillment"
        self.json = {"partnerUserId": str(uuid.uuid4())}

    def Generator(self):
        try:
            #Data.clearTerminal()
            while True:
                ctypes.windll.kernel32.SetConsoleTitleW(f"Opera GX Promos Generator | Genned: {Data.success} | Error: {Data.error}")
                response = self.client.post(self.url, json=self.json)
                if response.status_code == 200:
                    tokens = response.json().get('token')
                    url = f"https://discord.com/billing/partner-promotions/1180231712274387115/{tokens}"
                    Console.success(f"Successfully genned promos <> {tokens[0:50]}...")
                    open("Data/promos.txt", "a+").write(f"{url}\n")
                    Data.success += 1
                elif response.status_code == 429:
                    Data.error += 1
                    Console.error(f"You are being ratelimited")
                else:
                    Console.error(response.text)
                    Data.error += 1
        except Exception as e:
            Console.error(e)
            Data.error += 1

class Threading():
    def __init__(self) -> None:
        self.thread = Data.config['thread_count']

    def Start_Genning(self):
        try:
            start = Discord()
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread) as executor:
                for _ in range(self.thread):
                    executor.submit(start.Generator)
        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    Threading().Start_Genning()