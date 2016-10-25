#!/usr/bin/python

import time,sys,os,string

# This class encapsulates the data in the station_schedlinks.csv file, 
# and provides a function for determining what the current show is based
# on a time value represented as 'minutes into the week'

class schedule:

  def __init__(self, schedfile = ''):
    self.schedfile = schedfile
    self.schedlist = []
    schedfp = open(self.schedfile, "r")
    while(1):
      line = schedfp.readline()
      if not line:
        break
      tokens = line.split(';')
      seqnum = int(tokens[0].strip('"'))
      starttime = int(tokens[1].strip('"'))
      endtime = int(tokens[2].strip('"'))
      archname = os.path.basename(tokens[3].strip('"\r\n'))
      archname = archname[:-3] + 'mp3'
      self.schedlist.append([ starttime, endtime, archname ])
    print 'number of entries in schedule: %d' % len(self.schedlist)
    self.schedlist.sort()
    schedfp.close()
    sortfp = open("schedsort.csv", "w")
    for i in range(0, len(self.schedlist)):
      sortfp.write("%d, %d, %s\n" % (self.schedlist[i][0], self.schedlist[i][1], self.schedlist[i][2]))
    sortfp.close()


# for a given time (minutes into the week), return a list that contains 3 
# items: start time, end time, and archive file name.  All times are  
# represented as minutes into the week

  def currentshow(self, timenow):    
    for i in range(0, len(self.schedlist)):
      if self.schedlist[i][1] > timenow:
        break
    else:
      print 'time %d not found in list' % timenow
      return [ 0, 'sorry charlie' ]
    return self.schedlist[i]
    
# Return a list of two items: the number of minutes into the week RIGHT NOW,
# and the number of seconds past the minute RIGHT NOW

def GetCurrentMinutes():

  curtime = time.localtime()
  weekday = (curtime.tm_wday + 1) % 7
  curmin = (weekday * 1440) + (curtime.tm_hour * 60) + curtime.tm_min
  return [ curmin, curtime.tm_sec ]

# Initialize

mysched = schedule("./station_schedlinks.csv")
sys.stdout = open("./archlog", "w")


# Repeat ad infinitum

while(1):
  curminsec = GetCurrentMinutes()
  curmin = curminsec[0]
  cursec = curminsec[1]
  print "current week minutes is %d" % curmin
  print "current seconds is %d" % cursec
  curshow = mysched.currentshow(curmin)
  print 'current show is:'
  print curshow
  startmin = curshow[0]
  endmin = curshow[1]
  archivename = curshow[2]
  print "current show started at %d ends at %d" % (startmin, endmin)
  sleeptime = ( (endmin - curmin - 1) * 60 ) + (60 - cursec)
  print "sleep time is %d" % sleeptime
  archinternalname = "/home/archives/archive." + time.strftime("%Y-%m-%d-")
  time.sleep(sleeptime)
  print "Awake!!"
  print "archive external file name is " + archivename
# archivename is "5Fri-1430.1.mp3"
  arctokens = archivename.split('-')[1].split('.') 
# arctokens is ( "1430" "1" "mp4" )
  print arctokens
  if arctokens[1] == 'mp3':
     offset = 0
  else:
     offset = int(arctokens[1])
  archour = int(arctokens[0]) + (offset * 100)
  arcformat = format(archour / 100,"02d") + "-" + format(archour % 100, "02d") + ".mp3"
  archinternalname = archinternalname + arcformat
  print "internal name is " + archinternalname
  os.system("echo " + archinternalname + " >/tmp/darkice.file-0.`cat /var/run/darkice.pid`")
  os.system("kill -USR1 `cat /var/run/darkice.pid`")
  time.sleep(5)
  os.system("chmod a+r " + archinternalname)
  #os.spawnlp(os.P_NOWAIT, 'scp', 'scp', archinternalname, 'archivedeposit@130.245.253.140:~/archives/this_week/' + archivename) 
  os.spawnlp(os.P_NOWAIT, 'scp', 'scp', archinternalname, 'wusb@stream.wusb.stonybrook.edu:~/' + archivename) 
  


