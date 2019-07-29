

def repeat(string: str):

    len = string.__len__()

    for front in range(0, len + 1):
        for back in range(front + 1, len + 1):

            search = string[front:back]

            if string[back:].__contains__(search):

                print(search + " -- " + string[back:])


word = "herehere"
print(repeat(word))

# end of file

