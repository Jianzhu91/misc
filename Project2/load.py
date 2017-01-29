#! /usr/bin/env python
"""Name---Jian Zhu, Andrew ID----jianzhu"""

import os
from boto.ec2.connection import EC2Connection
import time
from urllib2 import urlopen
import myParser


LG = 'ami-4389fb26'
DC = 'ami-abb8cace'
KEY_NAME = 'project0_key1'
INSTANCE_TYPE = 'm3.medium' 
ZONE = 'us-east-1c'
SECURITY_GROUP_IDS = ['sg-29746f4e']
SUBNET_ID = 'subnet-9093d9bb'
DRY_RUN = True
DETAILED_MONITORING = True
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
SUBMISSION_CODE = os.environ['SUBMISSION_CODE']
TOTAL_DC = 0



# Launch a load generator
print 'Starting launch a load generator instance'
conn = EC2Connection(
    aws_access_key_id=AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
reservation = conn.run_instances(
    LG, 
    key_name=KEY_NAME, 
    placement=ZONE, 
    instance_type=INSTANCE_TYPE,
    subnet_id=SUBNET_ID,
    security_group_ids=SECURITY_GROUP_IDS,
    monitoring_enabled=DETAILED_MONITORING)
load_generator = reservation.instances[0]

while not load_generator.update() == 'running':
    time.sleep(2)
time.sleep(3)
load_generator.add_tag('Project', value='2.1')
load_generator_DNS = load_generator.dns_name
load_generator_ID = load_generator.id
print 'Having started the instance: ' + load_generator_ID \
+ ' DNS: {0}'.format(load_generator_DNS)


# Launch a data center
print 'Starting an DC instance with type {0}, image \
{1}'.format(INSTANCE_TYPE, DC)
reservation = conn.run_instances(
    DC, 
    key_name=KEY_NAME, 
    placement=ZONE, 
    instance_type=INSTANCE_TYPE,
    subnet_id=SUBNET_ID,
    security_group_ids=SECURITY_GROUP_IDS,
    monitoring_enabled=DETAILED_MONITORING)
data_center1 = reservation.instances[0]

while not data_center1.update() == 'running':
    time.sleep(2)
time.sleep(3)
data_center1.add_tag('Project', value='2.1')
data_center1_DNS = data_center1.dns_name
data_center1_ID = data_center1.id
print 'Having started the instance: ' + data_center1_ID + \
' DNS: {0}'.format(data_center1_DNS)


# Verify if the DC is running correctly
while True:
    isRunning = myParser.verify_instance_running(data_center1_DNS)
    if isRunning == True:
        break
    time.sleep(2)

# submit the password
ps_submit_url = 'http://' + load_generator_DNS + '/password?passwd=' \
+ SUBMISSION_CODE
time.sleep(2)
webpage = urlopen(ps_submit_url)
# start the test by submitting the 1st instance
dc1_submit_url = 'http://' + load_generator_DNS + '/test/horizontal?dns=' \
+ data_center1_DNS
time.sleep(2)
webpage = urlopen(dc1_submit_url)

# get the test-number
all_log_url = 'http://' + load_generator_DNS + '/log'
webpage = urlopen(all_log_url)
lines = webpage.readlines()
time.sleep(2)
test_number = myParser.parse_test_id(lines[0])
time.sleep(100)

# loop for aoto scaling
rps = 0
add_instances = []
while TOTAL_DC <= 6:
    rps = myParser.parse_log(load_generator_DNS, test_number)
    if rps >= 4000:
        break
    print 'Starting an new DC instance with type {0}, \
    image {1}'.format(INSTANCE_TYPE, DC)
    reservation = conn.run_instances(
        DC, 
        key_name=KEY_NAME, 
        placement=ZONE, 
        instance_type=INSTANCE_TYPE,
        subnet_id=SUBNET_ID,
        security_group_ids=SECURITY_GROUP_IDS,
        monitoring_enabled=DETAILED_MONITORING)
    tmp_dc = reservation.instances[0]
    add_instances.append(tmp_dc)
    time.sleep(2)

    while not add_instances[TOTAL_DC].update() == 'running':
        time.sleep(2)
    time.sleep(3)
    add_instances[TOTAL_DC].add_tag('Project', value='2.1')
    print 'Having started the instance: ' + add_instances[TOTAL_DC].id \
    + ' DNS: {0}'.format(add_instances[TOTAL_DC].dns_name)
    # Verify if the DC is running correctly
    while True:
        isRunning = myParser.verify_instance_running(add_instances[TOTAL_DC].dns_name)
        if isRunning == True:
            break
        time.sleep(2)

    add_dc_url = 'http://' + load_generator_DNS + '/test/horizontal/add?dns=' \
    + add_instances[TOTAL_DC].dns_name
    webpage = urlopen(add_dc_url)
    TOTAL_DC += 1
    time.sleep(100)


time.sleep(5)

raw_input('Please Enter to stop all the instances')
print 'Stop DC 1'
data_center1.stop()
print 'Stop Load generator'
load_generator.stop()
n = 0
while n < TOTAL_DC:
    print 'Stop DC: ' + add_instances[n].id
    add_instances[n].stop()
    n += 1