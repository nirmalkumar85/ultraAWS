#!/usr/bin/env python3.8
import boto3
import datetime
import os

def createzone(zonename):
    try:
        client = boto3.client("route53")
        response = client.create_hosted_zone(
            Name='airtickets.co.nz',
            CallerReference= 'test04',
            HostedZoneConfig={
                'Comment': 'Migrated from UltraDNS',
                'PrivateZone': False
            },
            #{
            #        "NameServers": [
            #            "ns-156.awsdns-19.com", 
            #            "ns-1620.awsdns-10.co.uk", 
            #            "ns-836.awsdns-40.net", 
            #            "ns-1183.awsdns-19.org"
            #        ], 
            #        "CallerReference": "HLO01", 
            #        "Id": "/delegationset/N081177417MRLQL7STVKJ"
            #    }
            DelegationSetId='N081177417MRLQL7STVKJ'
        )
        print(response)
        print("Importing Zone file...\n")
        command = "cli53 import --file zonefile/" + zonename + ".txt " + zonename
        #print(command)
        stream = os.popen(command)
        output = stream.read()
        print(output)

    except Exception as e: print(e)