#! python3
# phoneAndEmail.py - Finds phone numbers and email addresses on the clipboard.

import pyperclip
import re
import sys
from urllib.request import Request, urlopen

if len(sys.argv) < 2:
    print('Usage: python phoneAndEmail.py [link]')
    sys.exit()

# phone number regex, format (+48) 123 456 789 or +48 22 319 44 11
phoneRegex = re.compile(r'''(
    (\+\d{2}|\(\+\d{2}\))?          # area code
    (\s)?                           # separator
    (\d{2,4})                       # first 2 to 4 digits
    (\s)                            # separator
    (\d{2,4})                       # second 2 to 4 digits
    (\s)                            # separator
    (\d{2,4})                       # third 2 to 4 digits
    (\s)?                           # separator
    (\d{2,4})?                      # last 2 to 4 digits
    )''', re.VERBOSE)

# email address regex
emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+     # username
    @                     # @ symbol
    [a-zA-Z0-9.-]+        # domain name
    (\.[a-zA-Z]{2,4})     # dot-something
    )''', re.VERBOSE)

req = Request(sys.argv[1], headers={'User-Agent': 'Mozilla/5.0'})
text = str(urlopen(req).read())
matches = []

for groups in phoneRegex.findall(text):
    phoneNum = groups[0].strip()
    numbers = sum(c.isdigit() for c in phoneNum)

    if (numbers == 9 or numbers == 11) and phoneNum[0] != '0':
        matches.append(phoneNum)


for groups in emailRegex.findall(text):
    matches.append(groups[0])

matches = list(sorted(set(matches)))  # Remove duplicates and sort

# Copy results to the clipboard.
if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Phone numbers and emails addresses copied to clipboard:')
    print('\n'.join(matches))
else:
    print('No phone numbers or email addresses found.')
