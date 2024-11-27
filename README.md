# Wasac - Web Application Service Authentication Cracker


## What is it?
Wasac is a tool which is able to crack web applications' service authentication (such as crack passwod input box).

## What is the differences between Wasac and BurpSuite Intruder?
Wasac's cracking speed is much faster than BurpSuite Community Edition, because it has no limit and you don't need to pay money.

## How to use Wasac?
You can get help by passing in the **-h** parament, it will display help document.

```
python wasac.py -h
```
Let me show you an example about how to use this:

```
python wasac.py -t http://example.com/login --payload-count 2 -p1 /home/kali/usrname.txt -p2 /home/kali/passwd.txt -f "uname=^P1^&upass=^P2^" --grep-match incorrect
```
### About the method of how to set POST format
You'd better use Wireshark or BurpSuite to capture the POST request first. For example, the POST content is:

```
username=admin&password=123456&submit=Login
```
Repalce the payload poistion with **^P1^ and ^P2^**:

```
"username=^P1^&password=^P2^&submit=Login"
```
Then pass it into -f or --format parament.

## About author
Copyright (c) Gr3yPh 2024
MADE IN CHINA


**--THE END--**
