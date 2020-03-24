import sys

if len(sys.argv) != 2:
    print("usage: file.py filename")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename) as f:
        for line in f:
            # ignore comments
            comment_split = line.split('#')
            # strip whitespace
            num = comment_split[0].strip()
            # ignore blank lines
            if num == '':
                continue
            print(int(num, 2))

except FileNotFoundError:
    print('file not found')
    sys.exit(2)
