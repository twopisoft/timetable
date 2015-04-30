from openpyxl import Workbook, load_workbook
import random
import math
import sys

if len(sys.argv) <= 1:
    print 'Usage: python genparam.py <NUM_GROUPS> <NUM_TEACHERS>'
    sys.exit(0)

START = '80'
END = str(80+int(sys.argv[1])-1)
DAY_COL_START = 'K'
DAY_COL_END = 'O'
GROUP_COL = 'E'

GROUP_START = GROUP_COL + START
GROUP_END = GROUP_COL + END

DAY_START = DAY_COL_START + START
DAY_END = DAY_COL_END + END

GROUP_RANGE = GROUP_START + ':' + GROUP_END
DAY_RANGE = DAY_START + ':' + DAY_END

SLOTS = 4
NUM_TEACHERS = int(sys.argv[2])
SPECIAL_PERCENT = 20.0/100
MIN_HRS = 16
MAX_HRS = 26

print 'DAY RANGE={0}, NUM_TEACHERS={1}'.format(DAY_RANGE,NUM_TEACHERS)

EXCEL_FILE = 'sched.xlsx'
PARAM_FILE = 'big_{}.param'.format(NUM_TEACHERS)

print 'Reading Excel Data ...'

wb = load_workbook(EXCEL_FILE)

ws = wb.active

groups = []
for row in ws.iter_rows(GROUP_RANGE):
    for cell in row:
        groups.append(cell.value)

all_slots = []
for row in ws.iter_rows(DAY_RANGE):
    group_slots = []
    for cell in row:
        day_slots = [0]*SLOTS
        slots = cell.value.split(',')
        for slot in slots:
            s = slot.split('(')
            index = int(math.floor((int(s[0])-1)/2))
            #index = int(s[0])-1
            day_slots[index] = 1
        group_slots.append(day_slots)
    all_slots.append(group_slots)

print 'Generating Availability data ...'

special = random.sample(xrange(NUM_TEACHERS),int(math.ceil(NUM_TEACHERS*SPECIAL_PERCENT)))
availabilty = [[MIN_HRS,MAX_HRS]]*NUM_TEACHERS
for s in special:
    availabilty[s] = [MIN_HRS,MIN_HRS]

print 'Writing param file {0} ...'.format(PARAM_FILE)

with open(PARAM_FILE,'w') as outfile:
    outfile.write('letting NUM_GROUPS = {}\n'.format(len(all_slots)))
    outfile.write('letting NUM_TEACHERS = {}\n'.format(NUM_TEACHERS))
    outfile.write('\nletting Demand = ' + str(all_slots))
    outfile.write('\n\nletting Availability = ' + str(availabilty))

