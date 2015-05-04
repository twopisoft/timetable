from pyparsing import Word, Literal, alphas, OneOrMore, Optional, Group, SkipTo, Suppress
import sys

if len(sys.argv) != 5:
    print 'Usage: python verify.py <NUM_GROUPS> <NUM_TEACHERS> <Solution file> <Availability file>'
    sys.exit(0)

GROUPS = int(sys.argv[1])
TEACHERS = int(sys.argv[2])
SOLFILE = sys.argv[3]
AVAFILE = sys.argv[4]

SLOTS = 40
WKHRS = 16
MINHRS = 18
MAXHRS = 26

def __def_parser():

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
    matspec = SkipTo(left) + left + OneOrMore(vecspec.setResultsName('vec',listAllMatches=True) + Optional(comma)) + Suppress(typespec) + right

    return matspec

def __parse_data(f):
    data = ''
    with open(SOLFILE, 'r') as infile:
        data = infile.read().replace('\n','')

    result = __def_parser().parseString(data)

    roster = []
    for vec in result['vec']:
        str = ""
        for x in vec:
            str += x
        roster.append(eval(str))

    return roster

def __read_availability(f):
    data = ''
    with open(f,'r') as infile:
        data = infile.read().replace('\n','')

    return eval(data)

def test_group_hours(roster):
    data_ok = True

    for (i,g) in enumerate(roster):
        study_hrs = len(g) - g.count(0)
        if study_hrs != WKHRS:
            data_ok = False
            print "Group {0} hours not scheduled correctly: {1} != {2}".format(i+1,study_hrs,WKHRS)

    if data_ok:
        print "Groups Study Hours: Ok"

    return data_ok

def test_teacher_hours(roster,availability):
    data_ok = True

    t_hrs = { i:0 for i in range(1,TEACHERS+1) }
    for g in roster:
        for s in g:
            if s != 0:
                t_hrs[s] += 1

    for t in t_hrs.keys():
        if (t_hrs[t] < availability[t-1][0]) or (t_hrs[t] > availability[t-1][1]):
            data_ok = False
            print "Scheduled Hours for Teacher {0} violated: {1}: [{2},{3}]".format(t,t_hrs[t],availability[t-1][0],availability[t-1][1])

    if data_ok:
        print "Teacher Scheduled Hours: Ok"

    return data_ok

def test_teacher_clash(roster):
    data_ok = True

    for s in range(SLOTS):
        slot_assigns = [ roster[g][s] for g in range(GROUPS) if roster[g][s] != 0]
        if len(slot_assigns) > len(set(slot_assigns)):
            data_ok = False
            print "Clash detected on slot {0}".format(s)

    if data_ok:
        print "Clash detected: None"

    return data_ok

if __name__ == "__main__":

    print 'NUM_GROUPS={0}, NUM_TEACHERS={1}, SOLFILE={2}, AVAFILE={3}'.format(GROUPS,TEACHERS,SOLFILE,AVAFILE)

    roster = __parse_data(SOLFILE)

    availability = __read_availability(AVAFILE)

    test_group_hours(roster)
    test_teacher_hours(roster,availability)
    test_teacher_clash(roster)
