#!/usr/bin/env python

# 
# A test harness to see about converting text to a number and then
# counting it upwards.
# 

import re

pageMsg = "Page 1 of 4"

pageInfo = re.findall( r'\b\d+\b', pageMsg )
pageCount = int( pageInfo[1] )
print pageCount

