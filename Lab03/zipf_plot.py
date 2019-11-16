"""
USE: python <PROGNAME> (options) datafile1 ... datafileN
OPTIONS:
    -h : print this help message and exit
"""
################################################################

import sys, re, getopt
import pylab as p

opts, args = getopt.getopt(sys.argv[1:], 'h')
opts = dict(opts)
filenames = args

if '-h' in opts:
    progname = sys.argv[0]
    progname = progname.split('/')[-1]  # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit()

# + means 1 or more
# \w means all character
wordRE = re.compile('\w+')
wdCounts = {}
# Write a Python script to count all the word token occurrences in the ﬁle
# open the file from arg, then generate the dict
for filename in filenames:
    with open(filename) as infs:
        for line in infs:
            # map the input to lowercase, to conﬂate case variants.
            for wd in wordRE.findall(line.lower()):
                if wd not in wdCounts:
                    wdCounts[wd] = 0
                # Count the words into a dictionary
                wdCounts[wd] += 1

# then produce a list of the words sorted in descending order of frequency count
words = sorted(wdCounts, key=lambda x: wdCounts[x], reverse=True)
# 1 by n array
freqs = [wdCounts[w] for w in words]

# print out the total number of word occurrences from the data ﬁle
print('\nTypes: ', len(words))
print('Tokens: ', sum(freqs), '\n')
# the number of distinct words found
# and also 20 words with their frequencies
topN = 20
# words is a descending order of wdCounts
for wd in words[:topN]:
    print(wd, ':', wdCounts[wd])

################################################################
# Plot freq vs. rank

ranks = range(1, len(freqs) + 1)

p.figure()
p.plot(ranks, freqs)
p.title('freq vs rank')

################################################################
# Plot cumulative freq vs. rank

cumulative = list(freqs)  # makes copy of freqs list

for i in range(len(cumulative) - 1):
    cumulative[i + 1] += cumulative[i]

p.figure()
p.plot(ranks, cumulative)
p.title('cumulative freq vs rank')

################################################################
# Plot log-freq vs. log-rank

logfreqs = [p.log(freq) for freq in freqs]
logranks = [p.log(rank) for rank in ranks]

p.figure()
p.plot(logranks, logfreqs)
p.title('log-freq vs log-rank')
p.savefig('log1.png')

################################################################
# Display figures

p.show()

################################################################
