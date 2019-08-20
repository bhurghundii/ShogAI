with open('movesets.txt') as f:
    content = f.readlines()
    movesets = content[1].split('=')[1]
    #cast movesets to array
    print (movesets)

print ([(1,0), (-1,0)])
print type([(1,0), (-1,0)])
