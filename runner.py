import lib
import json
import datetime
import argparse
import os.path
import csv
#---Configuration options


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv', help='path to CSV file containing account ID and account group ID')
    args=parser.parse_args()
    
    if not os.path.exists(args.input_csv): #Verify that file exists
        parser.error("The file %s does not exist!" % args.input_csv)
    
    f=open(args.input_csv,'r')
    reader=csv.reader(f)#open as csv
    
    cfg=lib.config_helper.ConfigHelper()#get credentials for use with prisma cloud API
    
    
    sess=lib.redlock_sdk.RLSession(cfg.rl_user,cfg.rl_pass,cfg.rl_cust,cfg.rl_api_base)
    success = sess.authenticate_client()#get JWT for use in API
    
    if not success:
        print('Could not authenticate, check if your credentials in configs.yml are accurate.')
    else:
        print('Authentication complete')
        
        
    headers=next(reader) #Don't need headers for data parsing, assume file is formatted correctly
    
    list_of_acct_groups=json.loads(sess.interact('get','/cloud/group').text) #parse as json the list of account groups
    acct_group_id_to_name = { group['id']:group['name'] for group in list_of_acct_groups } #a dictionary that maps each account group ID to its name
    
    to_add={} #this dictionary is created for efficiency purposes, to minimize number of API calls
    
    
    for row in reader:
        acct_id,acct_group_id=row[0],row[1]
        
        if acct_group_id not in to_add:
            to_add[acct_group_id]=list()
        
        to_add[acct_group_id].append(acct_id) #for every account group, figure out all accounts that need to be added to it, instead of adding one at a time
                                              #This lets us call the API only once per account group, instead of once per account that needs to be added
    
    
    for group,accts_list in to_add.items(): #group is group id, accts_list is all accounts to add to that group
        resp=sess.interact('get','/cloud/group/%s'%(group))#get all accounts currently in group, so we can keep them
        
        json_data=json.loads(resp.text)
        accts_in_group=json_data['accountIds']
        accts_in_group.extend(accts_list) #add all accounts from csv file
        
        update_data={'id':group,        
                     'name':acct_group_id_to_name[group],
                     'accountIds':accts_in_group} #format as json to submit to server
        resp=sess.interact('put','/cloud/group/%s'%(group),reqbody=update_data)
    
    print('Done')
    
    
if __name__ == "__main__":
    main()
