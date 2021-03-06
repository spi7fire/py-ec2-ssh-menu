#!/usr/bin/env python2.7
import os
import boto3
import sys

pem_keys_path = '/home/ofershap/'

colors = {
        'blue': '\033[94m',
        'pink': '\033[95m',
        'green': '\033[92m',
        }

# we can filter the list by a word
filter = False
if len(sys.argv) > 1 :
    filter = sys.argv[1]
    print 'filtering by: ' + filter
 

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
 

def instances():
    # variables
    client = boto3.client('ec2')
    response = client.describe_instances()
    instancelist = []

    # loop
    for r in response['Reservations']:
        for i in r['Instances']:
            # show only instances with public ip
            if "PublicIpAddress" in i:
                instancename = ''
                # get tag name of instance
                for tags in i['Tags']:
                        if tags["Key"] == 'Name':
                            instancename = tags["Value"]
                # if there are args of filtering list then filter it
                if filter != False and filter not in instancename.lower():
                    continue
                # append instance to the list
                instance = {
                    'name': instancename,
                    'ip': i['PublicIpAddress'],
                    'key': i['KeyName'] + '.pem'
                }
                instancelist.append(instance)

    # return array of instances
    return instancelist

def main():
        servers = instances()
        print colorize('Select instance to SSH into:\n', 'green')
        for item in servers:
            print colorize("[" + str(servers.index(item)) + "] ", 'blue') + item['name']            
        choice = raw_input(">> ")
        try:
            if int(choice) < 0 : raise ValueError
            # Call the matching function
            selected = servers[int(choice)].values()
            command = 'ssh -i "'+pem_keys_path+selected[2]+'" ubuntu@'+selected[0];
            print 'calling ' + command
            os.system(command)
        except (ValueError, IndexError):
            print colorize('Wrong selection, exiting', 'pink')
 
if __name__ == "__main__":
    main()
