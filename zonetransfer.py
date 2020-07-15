#!/usr/bin/env python3.8
import dns.query, dns.zone, dns.resolver
import sys, socket, re, string
from aws_hostedzone_create import createzone
socket.setdefaulttimeout(10)

'''
  Get NS records
'''
def getNameservers(zonename):
    #Zonetransfer DNS server for your account
    nameservers = ["54.197.245.255"]
    try:
        #nameservers = dns.resolver.query(zonename, 'NS') 
        return nameservers    
    except dns.resolver.NoNameservers:
        print("\nDomain:", zonename, "has no ns records, sorry ;(")
        return ""

def getArgs():
    if  len(sys.argv) != 2:
        print('\n     Usage: \n\n     %s  fqdn\n' % sys.argv[0])
        print('\n     Purpose: \n\n     Test a domain for open zone transfer\n')
        sys.exit(1)
    else:
        zonename=re.sub('https://|http://|www.','',sys.argv[1])
        zonename=zonename.split('/')
        print("ZONENAME: %s" %zonename[0])
        return zonename[0]

def getZoneXfer(zonename):
    for nameserver in getNameservers(zonename):
        try:
            print('\nQuerying nameserver %s for DNS zone %s\r' % (nameserver,zonename))

            tryxfer = dns.zone.from_xfr(dns.query.xfr(str(nameserver), zonename))
            names = tryxfer.nodes.keys()
            #names.sort()
            sorted(names)
            f = open('zonefile/%s.txt' %(zonename),'w')

            for n in names:
                 #print(tryxfer[n].to_text(n))
                 f.write(tryxfer[n].to_text(n)+'\n')
                 #
            f.close()
            print('\nZone transferred from: ' + nameserver + '\n')
            print ('\n Creating AWS Zone')
            createzone(zonename)
        except dns.zone.NoNS:
            print("\nDomain: %s exists, but has no ns records, sorry ;( " %zonename)
        except dns.resolver.NXDOMAIN:
            print("\nDomain:", zonename, "unresponsive, try again\n")
        except dns.exception.FormError:
            print("\nXfer refused, good work dns admin\n")
        except EOFError:
            print("\nEOFError\n")
        except KeyboardInterrupt:
            print("\nUser cancelled\n")
        except KeyError as e: 
            print("KeyError %s" % e)
        except socket.error:
            print("\nFailed: connection refused\n")

zonename = getArgs()


'''
  Get nameserver records
'''

try:
    ns = getNameservers(zonename)
    if ns:
        print("Number of NS records: %s" % len(ns))
        getZoneXfer(zonename)

except dns.resolver.NXDOMAIN:
    print("AAA Invalid name %s" % zonename)
    sys.exit(1)

except dns.exception.Timeout:
    print("\nAAATimeout while attempting to contact DNS server")
    sys.exit(1)