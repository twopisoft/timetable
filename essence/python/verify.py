from pyparsing import Word, Literal, alphas, OneOrMore, Optional, Group, SkipTo, Suppress
import sys

if len(sys.argv) <= 1:
    print 'Usage: python verify.py <NUM_GROUPS> <NUM_TEACHERS>'
    sys.exit(0)

SLOTS = 4
TEACHERS = int(sys.argv[2])
DAYS = 5
GROUPS = int(sys.argv[1])

left = '['
right = ']'
digits = "0123456789"
comma = ","
semicolon = ";"
lparen = '('
rparen = ')'
intspec = 'int'
ellipses = '..'
varname = Word(alphas)
rangespec = Word(digits) + ellipses + Optional(Word(digits))
typespec = semicolon + intspec + lparen + rangespec + rparen
varspec = 'letting' + varname + 'be'
valspec = Word(digits) + Optional(comma)
vecspec = left + OneOrMore(valspec) + Suppress(typespec) + right
vecspecm = left + OneOrMore(vecspec.setResultsName('vec',listAllMatches=True) + Optional(comma)) + Suppress(typespec) + right
vecspecmm = left + OneOrMore(vecspecm + Optional(comma)) + Suppress(typespec) + right
matspec = SkipTo(left) + left + OneOrMore(vecspecmm + Optional(comma)) + Suppress(typespec) + right

solFile = 'big_{}.param.solution'.format(TEACHERS)

print 'NUM_GROUPS={0}, NUM_TEACHERS={1}, solFile={2}'.format(GROUPS,TEACHERS,solFile)

data = ''
with open(solFile, 'r') as infile:
    data = infile.read().replace('\n','')

result = matspec.parseString(data)

roster = [[[[0 for _ in range(SLOTS)] for _ in range(TEACHERS)] for _ in range(DAYS)] for _ in range(GROUPS)]

vecs = []
for vec in result['vec']:
    str = ""
    for x in vec:
        str += x
    vecs.append(eval(str))

for g in range(GROUPS):
    for d in range(DAYS):
        for t in range(TEACHERS):
            roster[g][d][t] = vecs[g*GROUPS*DAYS+d*TEACHERS+t]

tot = 0
for v in vecs:
    tot += sum(v)*2

print('\nTotal Hours scheduled: {0}'.format(tot))

rtot = 0
for g in range(GROUPS):
    for d in range(DAYS):
        for t in range(TEACHERS):
            rtot += sum(roster[g][d][t])*2

print('\nTotal Hours scheduled in roster: {0}'.format(rtot))  

print ('\nChecking for clashes...')

clashes = 0
for d in range(DAYS):
    for g in range(GROUPS):
        for t1 in range(TEACHERS):
            if roster[g][d][t1] == [0]*SLOTS:
                continue
            else:
                for t2 in range(t1+1,TEACHERS):
                    if roster[g][d][t2] == [0]*SLOTS:
                        continue
                    else:
                        clashes += 1 if roster[g][d][t1] == roster[g][d][t2] else 0

print ("{} clashes found".format(clashes))    

for g in range(GROUPS):
    th = 0
    for d in range(DAYS):
        for t in range(TEACHERS):
            th += sum(roster[g][d][t])*2
    print ("Group {} total hrs scheduled per week={}".format(g,th))

print ('\n')

for t in range(TEACHERS):
    th = 0
    for g in range(GROUPS):
        for d in range(DAYS):
            th += sum(roster[g][d][t])*2
    print ("Teacher {} total hrs scheduled per week={}".format(t,th))



  













