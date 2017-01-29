#! /usr/bin/env python
"""Name---Jian Zhu, Andrew ID----jianzhu"""

# from HTMLParser import HTMLParser
from urllib2 import urlopen
import ConfigParser


def parse_test_id(response):

    """This function is used to extract the test number from
    the log list page. It is a html page from:
    http://[your-load-generator-instance-dns-name]/log

    Args:
        response: the input string argument

    Returns:
        the test number in Integer format
    """


    start = response.find('>test')
    start += 6
    end = response.find('log<') - 1
    test_number = int(response[start:end])
    return test_number


def verify_instance_running(ec2_dns):

    """This function is used to verify whether the input instance is running
    correctly.

    Args:
        ec2_dns: the DNS name of input instance

    Returns:
        True: The instance is running correctly.
        False: The instance is still in process of setup.
    """


    url = 'http://' + ec2_dns + '/lookup/random'
    print url
    content = []
    try:
        webpage = urlopen(url, timeout=5)
        content = webpage.readlines()
    except IOError:
        print 'IOError'
        return False
    except Exception, e:
        print str(e)
        print 'time out'
        return False
    count = len(content)
    if count == 0:
        print count
        return False
    else:
        for line in content:
            line = line.strip()
            print line
            if line.startswith('Password'):
                return True
            else:
                return False



def parse_log(lg_dns, testID):

    """This function is used to parse the log file from 
    http://[load-generator-instance-dns-name]/log?name=test.[test-number].log
    It will return the recent total rps.

    Args:
        lg_dns: the DNS name of load generator
        testID: the test number

    Returns:
        True: The total rps.
    """

    url = 'http://' + lg_dns + '/log?name=test.' + str(testID) + '.log'
    webpage = urlopen(url)
    text = webpage.readlines()
    with open('log_lg.txt', 'w') as log:
        for line in text:
            if line.startswith('Your submission'):
                continue
            log.write(line)

    total = 0
    conf = ConfigParser.ConfigParser()
    conf.read('log_lg.txt')
    sections = conf.sections()
    last_section = ''
    for item in sections:
            last_section = item
    for opt in conf.options(last_section):
        num = conf.get(last_section, opt)
        total += float(num)
    print 'Total = ' + str(total)
    return total

