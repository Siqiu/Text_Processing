"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
OPTIONS:
    -h : print this help message
    -b : use BINARY weights (default: count weighting)
    -s FILE : use stoplist file FILE
    -I PATT : identify input files using pattern PATT, 
              (otherwise uses files listed on command line)
------------------------------------------------------------
"""

import sys, re, getopt, glob

class CommandLine:
    def __init__(self):
        # 'hs:bI:' opt h s b and I
        opts, args = getopt.getopt(sys.argv[1:], 'hs:bI:')
        opts = dict(opts)
        self.argfiles = args
        self.stops = set()
        self.binary_weights = False

        # HELP option
        if '-h' in opts:
            self.printHelp()
        if '-s' in opts:
            self.readStopList(opts['-s'])
        if '-b' in opts:
            self.binary_weights = True
        # Identify input files, when "-I" option used
        if '-I' in opts:
            self.argfiles = glob.glob(opts['-I'])

    def printHelp(self):
        progname = sys.argv[0]
        progname = progname.split('/')[-1]  # strip out extended path
        help = __doc__.replace('<PROGNAME>', progname, 1)
        print(help, file=sys.stderr)
        sys.exit()
    def readStopList(self, file):
        f = open(file, 'r')
        for line in f:
            self.stops.add(line.strip())

class Document:
    def __init__(self, file, stops):
        self.name = file
        self.counts = {}

        word = re.compile(r'[A-Za-z]+')

        f = open(file, 'r')
        for line in f:
            for wd in word.findall(line.lower()):
                if wd not in stops:
                    # judge whether the word is new
                    if wd in self.counts:
                        self.counts[wd] += 1
                    else:
                        self.counts[wd] = 1

    def get_Count(self, wd):
        return self.counts.get(wd, 0)

class CompareDocs:
    def __init__(self, config):
        self.argfiles = config.argfiles
        self.stops = config.stops
        self.binary_weights = config.binary_weights
        self.results = {}

    def jaccard(self, d1, d2):
        wds1 = set(d1.counts)
        wds2 = set(d2.counts)

        if self.binary_weights:
            # over is AB Intersection
            # under is AB union
            over = len(wds1 & wds2)
            under = len(wds1 | wds2)
        else:
            # question 8
            over = under = 0
            for w in (wds1 | wds2):
                over    += min(d1.get_Count(w), d2.get_Count(w))
                under   += max(d1.get_Count(w), d2.get_Count(w))

        if under > 0:
            return over / under
        else:
            return 0.0

    # Q9 eg NEWS/news01.txt <> NEWS/news02.txt = 0.017
    def compareAll(self):
        docs = []
        # generate the docs array
        for infile in self.argfiles:
            newdoc = Document(infile, self.stops)
            docs.append(newdoc)

        for i in range(len(docs)-1):
            d1 = docs[i]
            for j in range(i+1, len(docs)):
                d2 = docs[j]
                pair_name = '%s <> %s' % (d1.name, d2.name)
                self.results[pair_name] = self.jaccard(d1, d2)

    # Q9 the Q suggest top 10
    def printResults(self, stream=sys.stdout, topN=10):
        pairs = sorted(self.results, key=lambda v: self.results[v], reverse=True)
        if topN > 0:
            pairs = pairs[:topN]
        c = 0
        for k in pairs:
            c += 1
            print('(%d) %s = %.3f' % (c, k, self.results[k]), file=stream)


if __name__ == '__main__':
    config = CommandLine()
    compare = CompareDocs(config)
    compare.compareAll()
    compare.printResults()


# python compare.py -s stop_list.txt NEWS/news01.txt NEWS/news02.txt
# debug parameter
# python compare.py -s stop_list.txt -I NEWS/news??.txt
# python compare.py -s stop_list.txt -I NEWS/news0[123].txt
# terminal
# python compare.py -s stop_list.txt NEWS/news??.txt
# python compare.py -s stop_list.txt 'NEWS/news0[123].txt'

