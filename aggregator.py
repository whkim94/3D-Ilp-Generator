# -----------------------------------------------------------------------------
# Name:        aggregator.py
# Purpose:     implement a simple general purpose aggregator
#
# Author:   Jonathan Kim
# -----------------------------------------------------------------------------
"""
Implement a simple general purpose aggregator

Usage: aggregator.py filename topic
filename: input  file that contains a list of the online sources (urls).
topic:  topic to be researched and reported on

Get the command argument of filename sourcefile and topic
Open up the sourcefile and read each url
Use regular expression to get contents that contains topic in url text
If there is matching contents, open up new file and write it to it
Close the url
"""

import urllib.request
import urllib.error
import re
import sys

def aggregate(filename, topic):
    """
    Get filename and topic as arguments and make new file.
    """
    pattern = r'\>([^<]*\b{}\b.*?)\<'.format(topic)   # pattern
    with open(filename, 'r', encoding='utf-8') as file: # open file
        for url in file:    # for each url in file
            try:    # try exception handling
                with urllib.request.urlopen(url) as url_file: # open url
                    text = url_file.read().decode('UTF-8') # read all HTML
            except urllib.error.URLError as url_err: # if URLERROR
                print('Error opening url: ', url) # print error
                print(url_err)  # print error
            except UnicodeDecodeError as decode_err: # if decode error
                print('Error decoding url: ', url) # print error
                print(decode_err) # print error
            else:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                # find all pattern with the flag of case and newline
                with open(topic + 'summery.txt', 'a',encoding='utf-8') \
                        as out_file: # open output file
                    all_ref = '\n'.join(matches)    # join all matches
                    if matches: # if there is matches
                        out_file.write('Source url:')
                        out_file.write(url + '\n')
                        out_file.write(all_ref + '\n')
                        out_file.write('--------------------------------')
                        out_file.write('\n\n')  # write into file
                url_file.close()    # close url




def main():

    if len(sys.argv) != 3:  # Check for the right number of arguments
        print('Error: invalid number of arguments') # print error msg
        print ('Usage: aggregator.py filename topic') # print error msg
    else:
        filename = sys.argv[1]  # Get the filename argument
        topic = sys.argv[2]     # Get the topic argument
        aggregate(filename, topic) # call aggregate()



if __name__ == '__main__':
    main()