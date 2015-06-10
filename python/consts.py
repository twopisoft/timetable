# Number of slots (periods) per day
SLOTS = 12

# Number of days per week
DAYS = 5

# Total slots (periods) per week
WK_SLOTS = SLOTS * DAYS

# Number of study hours per week per group 
WEEK_HRS = 16

# Minimum teaching hours per week limit per teacher
MIN_HRS = 8

# Maximum teaching hours per week limit per teacher
MAX_HRS = 24

# Minimum teaching hours per day limit per teacher
MIN_HRSD = 2

# Maximum teaching hours per day limit per teacher
MAX_HRSD = 8

# Maximum teachers per group
MAX_TEACHERS = 5

# Data start row in input xlsx
START_ROW = 2
#START_ROW = 7

# Data end row in input xlsx
END_ROW = 100
#END_ROW = 69  # for subset version

# Day start column id in input xlsx file
DAY_START_COL = 'E'

# Day end column id in input xlsx file
DAY_END_COL = 'I'

# Group column id in input xlsx file
GROUP_COL = 'D'

# Course code column id in input xlsx file
COURSE_CODE_COL = 'A'

# Course name column id in input xlsx file
COURSE_NAME_COL = 'B'

# Weekdays names
WEEKDAYS = [u'Sunday',u'Monday',u'Tuesday',u'Wednesday',u'Thursday']

# Teacher Data Range
TEACHER_RANGE = 'A2:C77'
#TEACHER_RANGE = 'A10:C77'  # for subset version