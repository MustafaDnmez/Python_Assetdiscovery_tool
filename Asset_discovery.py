import dns.resolver
import sys
import nmap 
import httpx
# changed dns resolver lifretime from 5 to 10
# added google dns name server in resolver.py 

#read all subdomains
file = open(r"subdomains.txt").read()
# read all content
subdomains = file.splitlines()

def find_subdomain(domain):
    subdomain_store = []
   
    for subdoms in subdomains:
        try:
            full_domain=f'{subdoms}.{domain}'
            ip_value = dns.resolver.resolve(full_domain, 'A') # resolve domain 
            
            if ip_value:
                if f"{subdoms}.{domain}" in subdomain_store:
                    pass # if domain in list pass
                else:
                    ipadress="" # take resolved ip adress
                    for ip in ip_value:
                        ipadress=ip.to_text() #resolve ip address from ip_value opject
                    port=str(list(port_scan(ipadress))).replace(",",".")
                    url=str(find_url(full_domain)).replace(",",".")
                    subdomain_store.append(f'{full_domain},{ipadress},{port},{str(url)}') # append subdomain and ip address
                    
                    print(f'{full_domain},{ipadress},{(port)},{str(url)}')
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.NoAnswer:
            pass
        except KeyboardInterrupt:
            quit()
    output(subdomain_store)
def port_scan(target):
# instantiate a PortScanner object
    scanner = nmap.PortScanner()
    scanner.scan(target,None,"-v -sS --open")
    try:
        open_ports=scanner[target]["tcp"].keys()
    except:
        open_ports=""
    return open_ports

def find_url(domain):
   
    try:
        r=httpx.get(f"https://{domain}") # request the site and get response
        return [r.url,r.status_code]
    
    except :
     pass

def output(values):

    #save as csv
    with open("discovered_subdomains.csv", "a") as f:
     f.write("Subdomain,İp,Open_ports,Url/status")
     f.write("\n")
     for line in values:
        print(line, file=f)
try:
    domain = sys.argv[1] 
    #if input is a file open and read it by line
    if ".txt" in domain:
        text_file=[]
        with open(domain,"r") as file:
            text_file=file.readlines()
        for domains in text_file:
     
            find_subdomain(domains.strip())
    else:
        find_subdomain(domain)
except IndexError:
    print('Syntax Error - python3 subdomenum.py <domain or domains file with txt>')

