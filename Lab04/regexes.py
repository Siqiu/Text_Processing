# COM3110/4155/6155: Text Processing
# Regular Expressions Lab Class

import sys, re

# ------------------------------

# re.I means ignore upper or lower case
testRE = re.compile('(logic|sicstus)', re.I)


########################################################################################################################
# summary
# backref: () is the thing that u want
# \N: N = the number of () appears
# non-greedy by using ?
########################################################################################################################
# match the tag such as <sth>
RETag = re.compile(r"<.*?>", re.I)

# match the same item that appear several times.
# () is the item appear several times
# \1 in this code means (\w+)
REBackref = re.compile(r"<(\w+)>.*?</\1>")

# match the item appear between <\w+> and </\w+>
REMaterialInTag = re.compile(r"<\w+>(.*?)</\w+>")

# get url
REURL = re.compile(r"href=\"(.*?)\"")
########################################################################################################################

with open('RGX_DATA.html') as infs:
    linenum = 0
    for line in infs:
        linenum += 1
        if line.strip() == '':
            continue
        print('  ', '-' * 100, '[%d]' % linenum, '\n   TEXT:', line, end='')

        # match the first only
        # m = testRE.search(line)
        # if m:
        #     print('** TEST-RE:', m.group(1))

        # re.finditer(r"(\d+)@(\w+).com", content) (\d+) is group(1) (\w+) is group(2)

        # finditer will find all that matched
        # mm = testRE.finditer(line)
        # # we need to use the iter way to print out the item we matched
        # for m in mm:
        #     print('** TEST-RE:', m.group(1))

        # assigning them to variables with meaningful names
        # apply these RETag to each line of the ﬁle
        # printing out the matches that are found in the manner illustrated above.

        # printed out as "TAG: tag-string" (e.g. "TAG: b" for tag <b>).
        # assume <> symbol always appear at same line
        angleBrackets = RETag.finditer(line)
        for aB in angleBrackets:
            tag = aB.group(0)
            # Q1
            print('TAG: %s' % tag[1:-1])

            # Q3
            param = tag[1:-1].split(' ')
            # Q2 open and close brackets
            if tag[1] == '/':
                print("CLOSETAG:", param[0])
            else:
                print("OPENTAG:", param[0])
            if len(param) > 1:
                for p in param[1::]:
                    print("    PARAM: ", p)
            # print(RETag.findall(line))

            # Q4
            # < b > bold stuff < / b >
            # print the material that bet <b> and </b> as PAIR [b]: bold stuff.
            # print("\nPAIR", re.findall(REBackref, tag), ": ")
            pairs = REBackref.findall(line)
            if len(pairs) != 0:
                print("PAIR", pairs, ": ", REMaterialInTag.findall(line)[0])

            # Q5
            url = REURL.findall(line)
            if len(url) != 0:
                print("REURL: ", url[0])

            print("\n")

# Q6
with open('RGX_DATA.html') as infs:
    for line in infs:
        if line.strip() == '':
            continue
        print(RETag.sub("", line).strip())
