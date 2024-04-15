import argparse
import requests
import os
import sys
import random
from colorama import Fore

TestMandatorys = ['compilation', 'tests']

class TraceParser:
    def __init__(self, trace_data):
        self.winSize = os.get_terminal_size()
        self.trace_data = trace_data[len(trace_data) - 1]

        if not isinstance(self.trace_data, dict):
            raise ValueError('Trace is not a valid dictionary.')

        for mandatory_key in TestMandatorys:
            if mandatory_key not in self.trace_data:
                raise ValueError(f'Trace is missing mandatory key: {mandatory_key}')

        self.print_colorized_header()
        self.dump()

    def print_colorized_header(self):
        header_lines = (r"""
 $$$$$$\                                $$\ $$$$$$$\                            $$\      $$\                     $$\ $$\ 
$$  __$$\                               $$ |$$  __$$\                           $$$\    $$$ |                    $$ |\__|
$$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\  $$ |$$ |  $$ | $$$$$$\  $$\   $$\       $$$$\  $$$$ | $$$$$$\  $$\   $$\ $$ |$$\ 
$$ |      $$  __$$\ $$  __$$\ $$  __$$\ $$ |$$ |  $$ | \____$$\ $$ |  $$ |      $$\$$\$$ $$ |$$  __$$\ $$ |  $$ |$$ |$$ |
$$ |      $$ /  $$ |$$ /  $$ |$$ /  $$ |$$ |$$ |  $$ | $$$$$$$ |$$ |  $$ |      $$ \$$$  $$ |$$ /  $$ |$$ |  $$ |$$ |$$ |
$$ |  $$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$  __$$ |$$ |  $$ |      $$ |\$  /$$ |$$ |  $$ |$$ |  $$ |$$ |$$ |
\$$$$$$  |$$$$$$$  |\$$$$$$  |\$$$$$$  |$$ |$$$$$$$  |\$$$$$$$ |\$$$$$$$ |      $$ | \_/ $$ |\$$$$$$  |\$$$$$$  |$$ |$$ |
 \______/ $$  ____/  \______/  \______/ \__|\_______/  \_______| \____$$ |      \__|     \__| \______/  \______/ \__|\__|
          $$ |                                                  $$\   $$ |                                               
          $$ |                                                  \$$$$$$  |                                               
          \__|                                                   \______/
""").split('\n')

        for line in header_lines:
            self.shell_print(random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]) + line)
        self.shell_print(Fore.RESET)

    def shell_print(self, prompt):
        sys.stdout.write(f'{prompt}\n')

    def print_dict(self, data_dict):
        for key, value in data_dict.items():
            color = Fore.RED if 'KO' in value else Fore.GREEN
            self.shell_print(color + f'{key}: {value}')

    def dump(self):
        self.shell_print('=' * self.winSize.columns)
        self.shell_print('[COMPILATION]')
        self.print_dict(self.trace_data['compilation'])

        for binary, tests in self.trace_data['tests'].items():
            self.shell_print(Fore.RESET)
            self.shell_print('=' * self.winSize.columns)
            self.shell_print(f'[{binary}]')
            self.print_dict(tests)

def main():
    parser = argparse.ArgumentParser(description="Script d'analyse de traces")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--register", action="store_true", help="Effectuer l'enregistrement")
    group.add_argument("--result", action="store_true", help="Obtenir les résultats")

    args = parser.parse_args()

    if args.register:
        git_username = input("Veuillez entrer votre nom d'utilisateur Git : ")
        response = requests.post(f'http://193.70.40.62:5000/register/{git_username}', timeout=10)
        if response.status_code == 200:
            parsed_response = response.json()
            TraceParser(parsed_response)
        else:
            raise RuntimeError(f"Error {response.status_code} -> {str(response.json())}")
    elif args.result:
        git_username = input("Veuillez entrer votre nom d'utilisateur Git : ")
        response = requests.get(f'http://193.70.40.62:5000/mouli/{git_username}', timeout=10)
        if response.status_code == 200:
            trace_data = response.json()
            TraceParser(trace_data)
        else:
            raise RuntimeError(f"Error {response.status_code} -> {str(response.json())}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f'Erreur : {str(e)}\n')
        sys.exit(1)
