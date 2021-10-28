#!/usr/bin/python

import time,sys,os,string

# Return a list of two items: the number of minutes into the week RIGHT NOW,
# and the number of seconds past the minute RIGHT NOW

def GetCurrentMinutes():

  curtime = time.localtime()
  weekday = (curtime.tm_wday + 1) % 7
  curmin = (weekday * 1440) + (curtime.tm_hour * 60) + curtime.tm_min
  return [ curmin, curtime.tm_sec ]

# Take a string that is a time and a day of the week and return
# the number of minutes since midnight on Sunday morning 
def TimeToMin(intime, WeekDay):
  # Need to parse out the time, which is a number followed by 'am' or 'pm'
  AmPm = intime[-2:]
  # print "AmPm is '%s'\n" % AmPm
  if AmPm == "am":
    hours = 0
    timeHrs = intime[:-2].split(':')
    dayHrs = int(timeHrs[0])
    if dayHrs == 12:
      dayHrs = 0
    # print "am-timeHrs is " , timeHrs
    # print "am-intime is " + intime
    # print "2am-dayHrs is " + str(dayHrs)
  else:
    hours = 12
    timeHrs = intime[:-2].split(':')
    dayHrs = int(timeHrs[0])
    if dayHrs == 12:
      dayHrs = 0
    # print "pm-timeHrs is " , timeHrs
    # print "pm-intime is " + intime
  # Parse out timeHrs in case there's a colon
  hours += dayHrs
  if len(timeHrs) > 1:
    minutes = int(timeHrs[1])
  else:
    minutes = 0
  WeekInt = int(WeekDay) % 7
  minInWeek = (WeekInt * 1440) + (hours * 60) + minutes
  timeString = "0" + str((hours * 100) + minutes)
  # return [ minInWeek, hours[-2] + timeString[-4] ] 
  return [ minInWeek, timeString[-4:] ] 

def aQ(qstring):
    return '"' + str(qstring) + '"'

# Initialize

# Input and output
schedfp = open("website-schedule.txt", "r")
outschedfp = open("new-schedlink.csv", "w")
seq = 1
while(1):
    line = schedfp.readline()
    if not line:
       break
    # print line
    # Input line is time-range url (seperated by one space)
    linetok = line.split(' ')
    lineurl = linetok[1]
    dayOfWeek = lineurl.split('/')[4][:4]
    # print "dayOfWeek is %s\n" % dayOfWeek
    UrlbaseLen = len(os.path.basename(lineurl))
    # print "UrlbaseLen is %d\n" % UrlbaseLen
    Urlstem = lineurl[-UrlbaseLen]
    timerange = linetok[0].split('-')
    rangeBegin = timerange[0]
    rangeBeginMin = TimeToMin(rangeBegin, dayOfWeek[0])
    rangeEnd = timerange[1]
    rangeEndMin = TimeToMin(rangeEnd, dayOfWeek[0])
    # print "Range begin is %s" % rangeBeginMin
    # print "Range end is %s" % rangeEndMin
    nextline = aQ(seq) + ';' + aQ(rangeBeginMin[0]) + ';' + aQ(rangeEndMin[0]) + ';' + \
        aQ(lineurl[:-UrlbaseLen] + dayOfWeek+'-' + rangeBeginMin[1] + '.mp3') + '\n'
    outschedfp.write(nextline)
    seq += 1




