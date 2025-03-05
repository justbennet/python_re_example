import os
import re

verbose = False

file_name = 'sample.log'
timestamp = re.compile(r'(\d{2}:\d{2}:\d{2}) \(\w+\) TIMESTAMP (\d+/\d+/\d+)')
mlm_feature = re.compile('(\d{2}:\d{2}:\d{2}) \(MLM\) (\w+): \"(\S+)\" (\w+)@(\S+)')
lmgrd_start = re.compile('(\d{2}:\d{2}:\d{2}) \(lmgrd\) .* \(linux\) \((\d+/\d+/\d+)\)')
data = []
usage = {}
with open(file_name) as f:
    for line in f:
        if mlm_feature.match(line):
            p = mlm_feature.match(line)
            time = p.group(1)
            feature = p.group(3)
            user = p.group(4)
            host = p.group(5)
            if p.group(2) == 'OUT':
                data.append([date, time, feature, user, host])
                try:
                    usage[feature] += 1
                except KeyError:
                    usage[feature] = 1
                except:
                    print("WTF from trying an OUT record...?")
            elif p.group(2) == 'IN':
                data.append([date, time, feature, user, host])
                try:
                    usage[feature] -= 1
                except KeyError:
                    usage[feature] = 0
                    print("Just set", feature, "to 0 instead of negative")
                except:
                    print("WTF from trying an IN record...?")
            else:
                p = ''
                pass
            if verbose:
                print(data[-1][0], data[-1][1], data[-1][2], "current usage is", usage[feature])
        elif timestamp.match(line):
            p = timestamp.match(line)
            time = p.group(1)
            date = p.group(2)
        elif lmgrd_start.match(line):
            p = lmgrd_start.match(line)
            date = p.group(2)
            time = p.group(1)
            print(f"\n\nLicense server started on {date} at {time}")

print(f"\nData ends at {date} {time}")
print(f"Data contains {len(data)} entries in total")
print(f"\nHere are the first few lines of data\n")
for i in range(0,5):
    print(" ".join(data[i]))

print("\n\nPrinting usages for each feature\n" + "="*32 + '\n')
for key in sorted(usage.keys()):
    print(f"Feature {key:26}:  {usage[key]:<8}")

print("\n\n")
