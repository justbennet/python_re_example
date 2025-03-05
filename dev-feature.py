import os
import re

# Example of a feature checkout line
# 23:09:58 (MLM) OUT: "MATLAB" aquaman@monster.data.umich.edu  
#  NOTE:  There are actually a couple of spaces at the end of the line, so it
#  won't match when the $ terminator was in the re pattern.
#  You are warned about the dangers of invisible characters (spaces,tabs)!
#  This doesn't work because of the misplaced EOL indicator
#  mlm_feature = re.compile('(\d{2}:\d{2}:\d{2}) \(MLM\) (\w+): \"(\S+)\" (\w+)@(\S+)$')
mlm_feature = re.compile('(\d{2}:\d{2}:\d{2}) \(MLM\) (\w+): \"(\S+)\" (\w+)@(\S+)')
# mlm_feature(1) is the time
# mlm_feature(2) is OUT|IN
# mlm_feature(3) is the feature name
# mlm_feature(4) is the username
# mlm_feature(5) is the hostname

# Initialize an empty list
data = []

# Sample data
line = '23:09:58 (MLM) OUT: "MATLAB" aquaman@monster.data.umich.edu  '

# Use the compile RE on the line of sample data
p = mlm_feature.match(line)

# See definition of mlm_feature RE for what the elements are
data.append([ p.group(i) for i in range(1,6) ])

# What do we have
print(data)
