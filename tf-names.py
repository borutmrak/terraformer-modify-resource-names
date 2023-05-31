#!/usr/bin/env python3
#
# Import AWS Route53 resources to Terraform by using Terraformer
#
# Usage:
# terraformer plan aws -r route53 --profile <aws_profile> --regions <regions>
# ./rename_plan.py (this program renames resources that are generated on actual import, creates newplan.json)
# terraformer import plan newplan.json
# rm generated/aws/terraformer/provider.tf
# mv generated/aws/terraformer/*tf .
# terraform state replace-provider -auto-approve "registry.terraform.io/-/aws" "hashicorp/aws" # Needed because the state contains pre-0.13 names of providers. wtf?
#
# then terraform plan should show you no changes.

import json
import pprint
import sys
import re

pp = pprint.pprint

f = open("generated/aws/terraformer/plan.json","r")

j = json.loads(f.read())

j2 = []

for res in j['ImportedResource']['route53']:
    if res['InstanceInfo']['Type'] == 'aws_route53_zone':
        res['ResourceName'] = re.sub( r'tfer--[A-Z0-9]{12,}(.*)_', r'_\1', res['ResourceName'] )
        res['ResourceName'] = re.sub( r'-002E-', r'_', res['ResourceName'] )
        #print( "ZONE: %s %s" % (res['InstanceState']['attributes']['name'], res['ResourceName'] ) )
        #pp(res)
    elif res['InstanceInfo']['Type'] == 'aws_route53_record':
        res['ResourceName'] = re.sub( r'tfer--[A-Z0-9]{12,}_(.*)', r'_\1', res['ResourceName'] )
        res['ResourceName'] = re.sub( r'-002E-', r'_', res['ResourceName'] )
        res['Item']['zone_id'] = re.sub( r'tfer--[A-Z0-9]{12,}_(.*)', r'_\1', res['Item']['zone_id'] )
        res['Item']['zone_id'] = re.sub( r'-002E-', r'_', res['Item']['zone_id'] )
        #print( "RECORD: %s %s" % ( res['InstanceState']['attributes']['fqdn'], res['ResourceName'] ) )
        #pp(res)
        #break
    else:
        print( "WUT? UNKNOWN RESOURCE TYPE:" )
        pp(res)
        sys.exit(1)

    j2.append(res)

#pp(j2)
j['ImportedResource']['route53'] = j2

with open('newplan.json', 'wt') as out:
    out.write(json.dumps(j))
