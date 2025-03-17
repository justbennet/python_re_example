#!/bin/bash

# Regular expressions (REs) come if different flavors.  This is an example of
# using the sed flavor from a Linux command line.  sed REs are different
# from Python's, so I thought an example might be useful to see.

# Get the mac address from `ip addr` for just the net0 device
#
# ip addr returns information about all the network devices on a machine, e.g.
#
# $ip addr
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
#     link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
#     inet 127.0.0.1/8 scope host lo
#        valid_lft forever preferred_lft forever
# 2: net0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
#     link/ether 00:50:56:83:fc:ff brd ff:ff:ff:ff:ff:ff
#     inet 10.243.16.70/20 brd 10.243.31.255 scope global noprefixroute net0
#        valid_lft forever preferred_lft forever
# 3: net1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
#     link/ether 00:50:56:83:3b:0c brd ff:ff:ff:ff:ff:ff
#     inet 132.198.57.104/24 brd 132.198.57.255 scope global noprefixroute net1
#        valid_lft forever preferred_lft forever
#
# So, if we know the device name, we can use a modified version that just queries
# the device we care about.
#
# As you can see from the output above, that output is on more than one line.  When
# working with REs, it can often be simpler if they are all on one line, and saving
# the output to a variable will condense all whitespace to spaces.

if=$(ip addr show dev net0)

# The out contains an interface ID number followed by a colon-space
# Next comes the interface (if) name followed by a colon-space
# Then comes a lot of things we do not care about until we get to the
# first 'word' that contains colons, which will be the MAC address for
#   the interface, which we want to capture.
# Everything else, we don't care about
# In sed, 's/<match>/<substitute>/' is how you do search and replace
# Note that sed allows you to use an alternate delimiter, e.g.
# 's#<match>#<substitute>#' or 's=<match>=<substitute>='; using something
# other than / can be useful if you are working with file paths because
# you don't then have to escape `s/\/path\/to\/match/` becomes
# `s#/path/to/match#`.
# Inside the match, the ^ character outside a character group matches
# beginning of line.
# Next we match only numerals; the + is a sed special character meaning
# 'one or more' and must be escaped.  The ': ' following is literal
# text to be matched.
# We define 'capture groups using escaped parentheses, '\(<stuff to capture>\)';
# here we are looking for one or more words followed by a literal colon-space
# The the next group -- [^:] -- matches any characters except a colon.
# If ^ appears first inside a group definition, it negates the match.
# The [0-9a-z:] group matches numerals, lower-case alphabetical, and a colon,
# which is the format of the first MAC address; this works because it will
# match only a word because we have surrounded it by spaces.
# The .* matches everything else; use of * can be easily confused with
# shell glob use of *, so beware.  The . is the character class to match,
# the * says 'zero or more' of characters that match.
#
# We capture three things with \(<match string>\); in the replacement
# string, those are referred to by the index of the capture group, so
# we substitute just the first and third groups separated by ' # '.

echo $if | sed 's/^[0-9]\+: \(\w\+\): \([^:]\+\) link\/ether \([0-9a-z:]\+\) .*/\1 # \3/'






