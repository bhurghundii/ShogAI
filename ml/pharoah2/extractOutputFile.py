import re 

full_pattern = re.compile('[^a-zA-Z0-9\\\/.]|_')

def re_replace(string):
    return re.sub(full_pattern, '', string)

f = open("autoencoderoutput", "r")
s = f.readlines()

n = ""
for line in s:
	if "sample" in line:
		n += str(line)

print(type(n))

x = re_replace(n)
x = re.sub(r'\n\s*\n', '\n\n', x)

print(x)

m = []
c = 1
try:
	while True:
		m.append(x.split('loss')[c].split('acc')[1][:6])
		c = c + 1
		print(c)
except:
	pass
m = [v for i, v in enumerate(m) if i == 0 or v != m[i-1]]
print(m)

g = []
c = 1
try:
	while True:
		g.append(x.split('loss')[c].split('acc')[0])
		c = c + 1
		print(c)
except:
	pass

g = [v for i, v in enumerate(g) if i == 0 or v != g[i-1]]
print(g)

with open('modelloss.txt', 'w') as f:
    for item in g:
        f.write("%s\n" % item)

with open('modelacc.txt', 'w') as f:
    for item in m:
        f.write("%s\n" % item)

