#!/usr/bin/python3
import hashlib
import pyfiglet

ascii_banner = pyfiglet.figlet_format("TryHackMe \n Python 4 Pentesters \n HASH CRACKER for Sha1")
print(ascii_banner)

wordlist_location = str(input('Enter wordlist file location: '))
hash_input = str(input('Enter hash to be cracked: '))

with open(wordlist_location, 'r') as file:
    for line in file.readlines():
        plist = []
        plist.append(line.strip()+'robots.txt')
        plist.append(line.strip()+'.robots.txt')
        plist.append(line.strip().lower()+'robots.txt')
        plist.append(line.strip().lower()+'.robots.txt')
        plist.append(line.strip().upper()+'robots.txt')
        plist.append(line.strip().upper()+'.robots.txt')
        print(plist)
        for pelem in plist:
            hash_ob = hashlib.sha1(pelem.encode())
            hashed_pass = hash_ob.hexdigest()
            if hashed_pass == hash_input:
                print('Found cleartext password! ' + pelem)
                exit(0)
    print('Nem talált.')
