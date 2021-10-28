#!/usr/bin/python

# schedconvert.py - Convert schedule information copy/pasted from WUSB website
# to a schedlinks.csv file suitable for feeding into the archivespin.py program
# on the WUSB stream/archive server
# 
# Input - website-schedule.txt - This file is manually created by going to 
# the http://wusb.fm/admin/settings/station/schedlinks (login as an admin
# required) and copy/pasting each day's schedule links into a text file,
# then inserting a space before the "http" and deleting the blank lines
# 
# Output - new-schedlink.csv - This file has the start/end times for each 
# archive segment properly encoded as "minutes since midnight on Sunday",
# and also has the file name for the web link changed to follow the new name
# format - nddd-hhmm.mp3, where 'n' is the day of week (Sunday is 7, Monday
# through Saturday are 1 through 6), 'ddd' is the abbreviation of the day of 
# week (Sun, Mon, Tue, Wed, Thu, Fri, Sat), and hhmm is the time of the start
# of the archive segment.

import time,sys,os,string

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
  timeString = "0000" + str((hours * 100) + minutes)
  # return [ minInWeek, hours[-2] + timeString[-4] ] 
  return [ minInWeek, timeString[-4:] ] 

# Convert input to a string and put double quotes around it
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
    # There's an edge case where the end of the range is midnight (12am),
    # but the day of week is associated with the previous day, so we'll 
    # need to increment day of week in that particular case.
    rangeEnd = timerange[1]
    endDay = int(dayOfWeek[0])
    if rangeEnd == "12am":
      endDay += 1
    rangeEndMin = TimeToMin(rangeEnd, endDay)
    # print "Range begin is %s" % rangeBeginMin
    # print "Range end is %s" % rangeEndMin
    nextline = aQ(seq) + ';' + aQ(rangeBeginMin[0]) + ';' + aQ(rangeEndMin[0]) + ';' + \
        aQ(lineurl[:-UrlbaseLen] + dayOfWeek+'-' + rangeBeginMin[1] + '.mp3') + '\n'
    outschedfp.write(nextline)
    seq += 1




