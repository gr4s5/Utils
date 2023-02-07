#!/usr/bin/python3
import requests
import sys

proxy_address = ""
proxy_port = ""
proxy_address = "192.168.56.124"
proxy_port = "31337"

nrCLosed=0
nrFiltered=0
nrOpen=0

target = "127.0.0.1"
ports = range(1, 65536)

closed_message = "Connection refused"
acl_message = "Access Denied"

proxy = {
 "http": proxy_address+":"+proxy_port
}

open_ports = []
for port in ports:
    sys.stdout.write("Scan http://"+target+":"+str(port)+"\r")
    sys.stdout.flush()
    response = requests.get("http://"+target+":"+str(port), proxies=proxy)
    content = response.text
    if closed_message in content:
        #print("[-] Port "+str(port)+" is closed.")
        nrCLosed += 1
    elif acl_message in content:
        print("[!] Port "+str(port)+" is filtered.                       \r")
        nrFiltered += 1
    else:
        print("[+] Port "+str(port)+" is open.                      \r")
        open_ports.append(str(port))
        nrOpen += 1
print("Closed ("+str(nrCLosed)+"), Filtered ("+str(nrFiltered)+")")
print("Ports open ("+str(nrOpen)+"):")
print(open_ports)
