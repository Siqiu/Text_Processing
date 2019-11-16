import re

backRF1 = re.compile(r"<(\w+)> \1", re.I)


str1 = "<title>COM3290: Symbolic Reasoning</title>"
test = backRF1.findall(str1)
print(re.findall(re.compile(r"<(\w+)>.*?</\1>"), str1))
print(re.findall(re.compile(r"<\w+>(.*?)</\w+>"), str1))


str2 = '''
<a href="http://www.dcs.shef.ac.uk/~hepple/campus_only/sicstus_manual/sicstus4/index.html#Top">
'''
str3 = "<td> Dr Mark Hepple"
str4 = "<td> Dr Mark Hepple <td>"
str5 = "Dr Mark Hepple <td>"
print(re.findall(re.compile(r"<\w+>? ?(.*)?<\w+>?"), str5))




RETag = re.compile(r"<.*?>", re.I)
backRF = re.compile(r"<(\w+)>.*?</\1>")
materialInTag = re.compile(r"<\w+>(.*?)</\w+>")
URL = re.compile(r"href=\"(.*?)\"")

print(RETag.sub("", str4).strip())

str1 = ["bm3405", "dx19", "Thiscontainsav3440andsoqualifies"]

for i in str1:
    print(re.compile("[a-d][m-z][0-9]*").findall(i))

