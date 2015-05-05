from pyparsing import Word, Literal, alphas, OneOrMore, Optional, Group, SkipTo, Suppress
from openpyxl import Workbook, load_workbook
import sys
import argparse
import warnings

parser = argparse.ArgumentParser()
parser.add_argument("solution_file", help="Input Solution filename")
parser.add_argument("teacher_xlsx", help="Input Teacher xlsx filename")

args = parser.parse_args()

SLOTS = 40
WKHRS = 16
MINHRS = 18
MAXHRS = 26
MINHRSD = 2
MAXHRSD = 8
DAYS = 5
SLOTSD = 8

WEEKDAYS = ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY']

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

def parse_solution(f):
    data = ''
    with open(f, 'r') as infile:
        data = infile.read().replace('\n','')

    result = __def_parser().parseString(data)

    roster = []
    for vec in result['vec']:
        str = ""
        for x in vec:
            str += x
        roster.append(eval(str))

    return roster

def read_teachers(fname, read_names=False):

    print 'Reading Teacher Data ...'

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = load_workbook(filename=fname, read_only=True)

    ws = wb.active

    availability = []
    rows = list(ws.rows)
    num_ent = 3 if read_names else 2
    for row in rows[1:]:
        hrs = [0]*num_ent
        r = list(row)
        start_index = 0 if read_names else 1
        for (j,cell) in enumerate(r[start_index:]):
            hrs[j] = cell.value
        availability.append(hrs)

    return availability

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

    num_teachers = len(availability)
    t_hrs = { i:0 for i in range(1,num_teachers+1) }
    day_hrs = { i:[0]*DAYS for i in range(1,num_teachers+1) }

    for g in roster:
        for (i,s) in enumerate(g):
            if s != 0:
                t_hrs[s] += 1
                day = i/SLOTSD
                day_hrs[s][day] += 1  

    for t in t_hrs.keys():
        if (t_hrs[t] < availability[t-1][0]) or (t_hrs[t] > availability[t-1][1]):
            data_ok = False
            print "Scheduled Hours for Teacher {0} violated: {1}: [{2},{3}]".format(t,t_hrs[t],availability[t-1][0],availability[t-1][1])
        for d in range(DAYS):
            if (day_hrs[t][d] > 0) and ((day_hrs[t][d] < MINHRSD) or (day_hrs[t][d] > MAXHRSD)):
                data_ok = False
                print "Min/Max hours per day for Teacher {0} not fulfilled on {1}: {2}: [{3},{4}]".format(t,WEEKDAYS[d],day_hrs[t][d],MINHRSD,MAXHRSD)

    if data_ok:
        print "Teacher Scheduled Hours: Ok"

    return data_ok

def test_teacher_clash(roster):
    data_ok = True

    num_groups = len(roster)
    for s in range(SLOTS):
        slot_assigns = [ roster[g][s] for g in range(num_groups) if roster[g][s] != 0]
        if len(slot_assigns) > len(set(slot_assigns)):
            data_ok = False
            print "Clash detected on slot {0}".format(s)

    if data_ok:
        print "Clash detected: None"

    return data_ok

if __name__ == "__main__":

    roster = parse_solution(args.solution_file)

    availability = read_teachers(args.teacher_xlsx)

    test_group_hours(roster)
    test_teacher_hours(roster,availability)
    test_teacher_clash(roster)
