"""
USE: python <PROGNAME> (options) 
OPTIONS:
    -h : print this help message and exit
    -d FILE : use FILE as data to create a new lexicon file
    -l FILE : create OR read lexicon file FILE
    -t FILE : apply lexicon to test data in FILE
"""
################################################################

import sys, re, getopt

################################################################
# Command line options handling, and help

opts, args = getopt.getopt(sys.argv[1:], 'hd:t:')
opts = dict(opts)


def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1]  # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit()


if '-h' in opts:
    printHelp()

if len(args) > 0:
    print("\n** ERROR: no arg files - only options! **", file=sys.stderr)
    printHelp()

if '-d' not in opts:
    print("\n** ERROR: must specify training data file (opt: -d FILE) **", file=sys.stderr)
    printHelp()


################################################################

# training data ﬁle,
# splitting each sentence into its tokens
# and counting the co-occurence of tokens and POS tags.


# splitting sentence into its tokens and pos, by using '/' symbol
def parseLine(line):
    wdtags = line.split()
    wdtagpairs = []
    for wdtag in wdtags:
        # split the TOKEN/POS
        parts = wdtag.split('/')
        # append to the word tag pairs
        wdtagpairs.append((parts[0], parts[1]))
    return wdtagpairs


################################################################
# 6 (a)
# and counting the co occurence of tokens and POS tags.
# This is main data structure -a two-level dictionary,
# mapping {words -> {tag -> counts}}
wordTagCounts = {}

print('<reading data for new lexicon ....>', file=sys.stderr)
with open(opts['-d']) as data_in:
    # each line in file (data_in)
    for line in data_in:
        # splitting the token and tags
        for (wd, tag) in parseLine(line):
            # if wd == 'the':
            #     print(True)
            # word whether exist
            if wd not in wordTagCounts:
                wordTagCounts[wd] = {}
            # whether tag already exist
            # if tag already exist, tag +=1
            if tag in wordTagCounts[wd]:
                wordTagCounts[wd][tag] += 1
            # if tag not exist, init the new tag
            else:
                wordTagCounts[wd][tag] = 1
print('<done>', file=sys.stderr)

################################################################
# ANALYSE word-tag-count dictionary, to compute:
# 6 (b)
# -- proportion of types that have more than one tag
# 7
# -- accuracy naive tagger would have on the training data
# -- most common tags globally
tagCounts = {}
ambiguousTypes = 0
ambiguousTokens = 0
allTypes = len(wordTagCounts)
allTokens = 0
correctTokens = 0

for wd in wordTagCounts:
    values = wordTagCounts[wd].values()

    # len(values) > 1 it means: same word has different meaning
    if len(values) > 1:
        ambiguousTypes += 1
        ambiguousTokens += sum(values)

    # most common POS tag
    correctTokens += max(values)
    allTokens += sum(values)
    # t: tag    c: count
    # count the num of tag that appears
    for t, c in wordTagCounts[wd].items():
        if t in tagCounts:
            tagCounts[t] += c
        else:
            tagCounts[t] = c

print('Proportion of word types that are ambiguous: %5.1f%% (%d / %d)' % \
      ((100.0 * ambiguousTypes) / allTypes, ambiguousTypes, allTypes), file=sys.stderr)

print('Proportion of tokens that are ambiguous in data: %5.1f%% (%d / %d)' % \
      ((100.0 * ambiguousTokens) / allTokens, ambiguousTokens, allTokens), file=sys.stderr)

print('Accuracy of naive tagger on training data: %5.1f%% (%d / %d)' % \
      ((100.0 * correctTokens) / allTokens, correctTokens, allTokens), file=sys.stderr)

tags = sorted(tagCounts, key=lambda x: tagCounts[x], reverse=True)
print('Top Ten Tags by count:', file=sys.stderr)
for tag in tags[:10]:
    count = tagCounts[tag]
    print('   %9s %6.2f%% (%5d / %d)' % \
          (tag, (100.0 * count) / allTokens, count, allTokens), file=sys.stderr)

################################################
# apply the naive tagging approach to the [test data],
# using the counts derived from the training data
# Function to 'guess' tag for unknown words
# i.e. words that were not seen in the training data

digitRE = re.compile('\d')
jj_ends_RE = re.compile('(ed|us|ic|ble|ive|ary|ful|ical|less)$')


# Begin by assuming that all unknown words are tagged incorrectly,
# by assigning them a non-PTB-tag symbol, such as UNK, as their POS tag).
# Determine the tagging accuracy this method achieves over the test data.

# NOTE: if you uncomment the 'return' at the start of the following
# definition, the score achieved will be that where all unknown words
# are tagged *incorrectly* (as UNK). Uncommenting instead the third
# 'return', will yield the score where the default tag for unknown
# words is NNP. Otherwise, the definition attempts to guess the
# correct tags for unknown words based on their suffix or other
# characteristics.

# first assign each unknown word the most common tag overall (which you should have determined above)

def tagUnknow(wd):
    #    return 'UNK' unknown token
    #    return 'NN'
    #    return 'NNP'
    if wd[0:1].isupper():
        return "NNP"
    if '-' in wd:
        return 'JJ'
    if digitRE.search(wd):
        return 'CD'
    if jj_ends_RE.search(wd):
        return 'JJ'
    if wd.endswith('s'):
        return 'NNS'
    if wd.endswith('ly'):
        return 'RB'
    if wd.endswith('ing'):
        return 'VBG'


################################################
# Apply naive tagging method to test data, and score performance
if '-t' in opts:
    # assign each unknown word the 'most common' tag overall
    # most common wd store in max tag dict
    maxTag = {}
    for wd in wordTagCounts:
        # find the most common tag in the word
        tags = sorted(wordTagCounts[wd], key=lambda x: wordTagCounts[wd][x], reverse=True)
        maxTag[wd] = tags[0]

    print('<tagging test data .....>', file=sys.stderr)

    # Tag each word of the test data, and score
    # opts['-t'] is the file name that after arg '-t'. 'r' is read mode(default parameter)
    test = open(opts['-t'])
    allTest = 0
    correct = 0

    for line in test:
        # the func of parseLine is split the line by using /
        # for loop the opt each wd and tag
        for wd, trueTag in parseLine(line):
            # the wd in most Common dict
            if wd in maxTag:
                newTag = maxTag[wd]
            else:
                newTag = tagUnknow(wd)
            allTest += 1
            if newTag == trueTag:
                correct += 1
    print('<done>', file=sys.stderr)

    print("Score on test data: %5.1f%% (%5d / %5d)" % \
          ((100.0 * correct) / allTest, correct, allTest), file=sys.stderr)

################################################
print('<done>')
