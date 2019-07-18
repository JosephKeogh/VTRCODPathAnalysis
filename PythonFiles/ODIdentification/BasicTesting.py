

string = "PathID: I-66-WB Count: 1"

countIndex = string.index("Count:")
path = string[8:countIndex-1]
count = string[countIndex+7:]


print("'" + path + "'")
print("'" + count + "'")

# end of file
