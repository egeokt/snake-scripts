""" 
You're building a feature to improve how ls -l output is displayed in the terminal. 
Write a Python function that parses the raw output of ls -l (as a string), and 
returns a list of dictionaries for each file.



Example input:

-rw-r--r--  1 user staff   1048576 Jun 10 12:00 report.pdf
drwxr-xr-x  3 user staff       96 Jun  9 09:21 photos

Expected output:

[
  {
    "type": "file",
    "permissions": "-rw-r--r--",
    "links": 1,
    "owner": "user",
    "group": "staff",
    "size": 1048576,
    "modified": "Jun 10 12:00",
    "name": "report.pdf"
  },
  {
    "type": "directory",
    ...
  }
]



"""

"""
Approach:
1. Understand what's in the ls -l output:
   - Permissions (e.g., -rw-r--r--) get the first character to determine if it's a file or directory or something else
   - Number of links
   - Owner
   - Group
   - Size in bytes
   - Last modified date and time
   - File or directory name
   there can also be a line which starts with 'total' which we can ignore.
   can we have a file that has no name? or folder that has no name?

2. ignore the first line if it starts with 'total'.
3. split the input into lines
4. for each line, split that into the components like above.
5. create a dictionary item for each line with the 
"""

import subprocess
import sys


def parse_ls_output(ls_output: str) -> list:
    lines = ls_output.strip().split('\n')

    result = []

    for line in lines:
        if line.startswith('total'):
            continue

        parts = line.split()

        # get the parts of the line
        permissions = parts[0]
        links = int(parts[1])
        owner = parts[2]
        group = parts[3]
        size = int(parts[4])
        modified_at = ' '.join(parts[5:8])
        name = ' '.join(parts[8:])

        # determine the type
        if permissions.startswith('d'):
            file_type = 'directory'
        elif permissions.startswith('-'):
            file_type = 'file'
        else:
            file_type = 'other'

        # create the dictionary for this file
        file_info = {
            "type": file_type,
            "permissions": permissions,
            "links": links,
            "owner": owner,
            "group": group,
            "size": size,
            "modified": modified_at,
            "name": name
        }
        result.append(file_info)

    return result


if __name__ == '__main__':

    if len(sys.argv) > 2:
        print("Usage: python ls-parser.py [optional: directory]")
        sys.exit(1)
    ls_output = ''
    if len(sys.argv) == 2:
        directory = sys.argv[1]
        print(f'Running ls -l command on {directory}...\n')

        sub_result = subprocess.run(
            ["ls", "-l", directory], capture_output=True, text=True)
        ls_output = sub_result.stdout
    else:
        print('Running ls -l command in the current directory...\n')
        sub_result = subprocess.run(
            ["ls", "-l"], capture_output=True, text=True)
        ls_output = sub_result.stdout

    parsed_output = parse_ls_output(ls_output)
    for item in parsed_output:
        print(item)
