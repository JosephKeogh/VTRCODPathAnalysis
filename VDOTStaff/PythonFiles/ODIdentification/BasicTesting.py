import sys

sys.argv.pop(0)
filename = sys.argv.pop(0)
with open(filename, 'r') as file:
    print(file.readline())
file.close()
# end of file
