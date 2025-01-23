# Copyright © Gr3yPh 2024. All rights reserved.

import argparse
import requests
import sys
import os
import shutil
import logging
import concurrent.futures
from urllib.parse import urlparse

# ANSI 转义序列
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    WHITE = '\033[97m'

def clear_screen():
    # 清屏处理
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    # 居中显示文本
    term_width = shutil.get_terminal_size().columns
    return text.center(term_width)

def print_banner():
    print(center_text(Colors.GREEN + 'WASAC'))
    print(center_text('Web Application Service Authentication Cracker v1.0'))
    print(center_text('Copyright (c) Gr3yPh 2024'))
    print(center_text('GitHub: http://github.com/Gr3yPh/wasac'))
    print()
    # 将字体颜色切换为白色
    print(Colors.WHITE, end='')

def load_payloads(payload_file):
    try:
        with open(payload_file, 'r') as f:
            payloads = [line.strip() for line in f]
        if not payloads:
            logging.error(f'Payload file {payload_file} is empty.')
            sys.exit(1)
        return payloads
    except IOError:
        logging.error(f'Error opening file: {payload_file}. Please check if the file is valid.')
        sys.exit(1)

def send_request(target, data, headers):
    try:
        response = requests.post(target, headers=headers, data=data, timeout=10)
        return response
    except requests.Timeout:
        logging.error('Request timed out.')
    except requests.ConnectionError:
        logging.error('Network problem (e.g., DNS failure, refused connection, etc).')
    except requests.RequestException as e:
        logging.error(f'An error occurred: {e}')
    return None

def log_sanitized(payload, data, response, is_failed):
    status = 'Failed' if is_failed else 'Success'
    logging.info(f'Payload: {payload} | Request Data: {data} | Response Length: {len(response.text) if response else "N/A"} | Status: {status}')

def worker(target, payload, format_str, headers, grep_match, first):
    data = format_str.replace('^P1^', payload)
    response = send_request(target, data, headers)
    if response:
        is_failed = grep_match.encode() in response.content
        log_sanitized(payload, data, response, is_failed)
        return (payload, len(response.text), is_failed, response.text)
    return (payload, 0, True, '')

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="A tool to crack web applications' service authentication")
    parser.add_argument('-t', '--target', type=str, required=True, help='Target URL')
    parser.add_argument('--payload-count', type=int, choices=[1, 2], required=True, help='Payload count (1 or 2)')
    parser.add_argument('-p1', '--payload1', type=str, help='The path of the first payload\'s dictionary')
    parser.add_argument('-p2', '--payload2', type=str, help='The path of the second payload\'s dictionary')
    parser.add_argument('-f', '--format', type=str, required=True, help='POST Format (replace payload position with ^P1^ and ^P2^)')
    parser.add_argument('-F', '--First', action='store_true', help='Stop cracking as soon as the first valid payload is found')
    parser.add_argument('--grep-match', type=str, help='Flag items that contain this value', default='failed')
    parser.add_argument('-o', '--output', type=str, help='Output file to save detailed logs')
    parser.add_argument('--max-workers', type=int, default=10, help='Maximum number of worker threads')
    args = parser.parse_args()

    logging.basicConfig(filename=args.output if args.output else 'wasac.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    count = success_count = fail_count = 0
    successful_payloads = []

    # 输出目标和加载的 payload 数量
    print(center_text(f'Target URL: {args.target}'))
    print(center_text('Loading Payloads...'))

    if args.payload_count == 1:
        payloads = load_payloads(args.payload1)
        print(center_text(f'Loaded {len(payloads)} payloads from {args.payload1}'))
        print(center_text('-' * 80))

        print(center_text(f'{"Payload":<30} | {"Response Length":<20} | {"Status":<10}'))
        print(center_text('-' * 80))

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            futures = {executor.submit(worker, args.target, payload, args.format, headers, args.grep_match, args.First): payload for payload in payloads}
            for future in concurrent.futures.as_completed(futures):
                payload, response_length, is_failed, response_text = future.result()
                if is_failed:
                    print(center_text(f'{Colors.WHITE}{payload:<30} | {response_length:<20} | {Colors.RED}Failed{Colors.RESET}'))
                    fail_count += 1
                else:
                    print(center_text(f'{Colors.WHITE}{payload:<30} | {response_length:<20} | {Colors.GREEN}Success{Colors.RESET}'))
                    success_count += 1
                    successful_payloads.append(payload)
                    if args.First:
                        break

    elif args.payload_count == 2:
        payloads1 = load_payloads(args.payload1)
        payloads2 = load_payloads(args.payload2)
        print(center_text(f'Loaded {len(payloads1)} payloads from {args.payload1} and {len(payloads2)} payloads from {args.payload2}'))
        print(center_text('-' * 80))

        print(center_text(f'{"Payload 1":<30} | {"Payload 2":<30} | {"Response Length":<20} | {"Status":<10}'))
        print(center_text('-' * 80))

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            futures = {executor.submit(worker, args.target, payload1, args.format.replace('^P2^', payload2), headers, args.grep_match, args.First): (payload1, payload2)
                       for payload1 in payloads1 for payload2 in payloads2}
            for future in concurrent.futures.as_completed(futures):
                payload1, payload2 = futures[future]
                payload, response_length, is_failed, response_text = future.result()
                if is_failed:
                    print(center_text(f'{Colors.WHITE}{payload1:<30} | {Colors.WHITE}{payload2:<30} | {response_length:<20} | {Colors.RED}Failed{Colors.RESET}'))
                    fail_count += 1
                else:
                    print(center_text(f'{Colors.WHITE}{payload1:<30} | {Colors.WHITE}{payload2:<30} | {response_length:<20} | {Colors.GREEN}Success{Colors.RESET}'))
                    success_count += 1
                    successful_payloads.append((payload1, payload2))
                    if args.First:
                        break

    print(center_text(Colors.YELLOW + '\n' + '*' * 25 + '\n'))
    print(center_text(Colors.GREEN + '[+] Finished.'))
    print(center_text(f'[*] Total {count}'))
    print(center_text(f'[*] Success count {success_count}'))
    print(center_text(f'[*] Failure count {fail_count}'))
    
    print(center_text(Colors.WHITE + '\n[*] Successful Payloads: ' + ', '.join(map(str, successful_payloads))))

if __name__ == "__main__":
    main()
