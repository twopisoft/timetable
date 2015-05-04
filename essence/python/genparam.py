from openpyxl import Workbook, load_workbook
import random
import math
import sys
import warnings

if len(sys.argv) < 4:
    print 'Usage: python genparam.py <NUM_GROUPS> <NUM_TEACHERS> <input xslx file> [<output param file>] [<availabilty file>]'
    sys.exit(0)

NUM_GROUPS = int(sys.argv[1])
NUM_TEACHERS = int(sys.argv[2])
EXCEL_FILE = sys.argv[3]

START = '80'
END = str(80+NUM_GROUPS-1)
DAY_COL_START = 'K'
DAY_COL_END = 'O'
GROUP_COL = 'E'

GROUP_START = GROUP_COL + START
GROUP_END = GROUP_COL + END

DAY_START = DAY_COL_START + START
DAY_END = DAY_COL_END + END

GROUP_RANGE = GROUP_START + ':' + GROUP_END
DAY_RANGE = DAY_START + ':' + DAY_END

SLOTS = 8
DAYS = 5
WEEK_HRS = 16

SPECIAL_PERCENT = 20.0/100
MIN_HRS = 18
MAX_HRS = 26

WEEKDAYS = ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY']

def __flatten(l):
    return [j for i in l for j in i]

def __read_slots(ws):
    all_slots = []
    for (i,row) in enumerate(ws.iter_rows(DAY_RANGE)):
        group_slots = []
        for cell in row:
            day_slots = [0]*SLOTS
            slots = cell.value.split(',')
            for slot in slots:
                s = slot.split('(')
                #index = int(math.floor((int(s[0])-1)/2))
                index = int(s[0])-1
                day_slots[index] = 1
            group_slots.append(day_slots)
        all_slots.append(__flatten(group_slots))

    return all_slots

def __availability():
    print 'Generating Availability data ...'

    special = random.sample(xrange(NUM_TEACHERS),int(math.ceil(NUM_TEACHERS*SPECIAL_PERCENT)))
    availabilty = [[MIN_HRS,MAX_HRS]]*NUM_TEACHERS
    for s in special:
        availabilty[s] = [MIN_HRS,MIN_HRS]

    return availabilty

def write_param_file(all_slots,availabilty):

    if len(sys.argv) >= 5:
        PARAM_FILE = sys.argv[4]

        print 'Writing param file "{0}" ...'.format(PARAM_FILE)
        with open(PARAM_FILE,'w') as outfile:
            outfile.write('letting NUM_GROUPS = {}\n'.format(len(all_slots)))
            outfile.write('letting NUM_TEACHERS = {}\n'.format(NUM_TEACHERS))
            outfile.write('\nletting Demand = ' + str(all_slots))
            outfile.write('\n\nletting Availability = ' + str(availabilty))

def write_availability_file(availability):
    if len(sys.argv) >= 6:
        AVAILABILITY_FILE = sys.argv[5]

        print 'Writing Availability file "{0}" ...'.format(AVAILABILITY_FILE)
        with open(AVAILABILITY_FILE,'w') as outfile:
            outfile.write(str(availability))

def test_resource_match(all_slots) :

    data_ok = True

    for s in range(SLOTS*DAYS):
        busy_slots = 0
        for (i,g) in enumerate(all_slots):
            busy_slots += all_slots[i][s]

        if busy_slots > NUM_TEACHERS:
            data_ok = False
            print 'Found resource mismatch on {0} for slot {1}. busy_slots={2}, NUM_TEACHERS={3}'.format(WEEKDAYS[s/SLOTS],s,busy_slots,NUM_TEACHERS)

    if data_ok:
        print 'Resource match check: Ok'

    return data_ok

def test_week_hrs(all_slots):

    data_ok = True

    for (i,s) in enumerate(all_slots):
        hrs = s.count(1)
        if hrs != WEEK_HRS:
            data_ok = False
            print "Not enough hours for group {0}. {1} != {2}".format(i+1,hrs,WEEK_HRS)

    if data_ok:
        print "Hours Scheduled: Ok"

    return data_ok

if __name__ == "__main__":

    print 'DAY RANGE={0}, NUM_GROUPS={1}, NUM_TEACHERS={2}'.format(DAY_RANGE,NUM_GROUPS,NUM_TEACHERS)

    print 'Reading Excel Data ...'

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = load_workbook(filename=EXCEL_FILE, read_only=True)

    ws = wb.active

    all_slots = __read_slots(ws)
    availability = __availability()

    test_resource_match(all_slots)
    test_week_hrs(all_slots)

    write_param_file(all_slots,availability)
    write_availability_file(availability)
