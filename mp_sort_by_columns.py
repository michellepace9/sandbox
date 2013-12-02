import sys

IN_FILE = sys.argv[1]
TIME_COL = 0; USERID_COL = 2;

def user_id_and_time(row):
	fields = row.split(',')
	userid = long(fields[USERID_COL]) if len(fields[USERID_COL])>0 else ''
	return (userid, fields[TIME_COL])

def sort(inputfile):
	with open(inputfile) as f:
		data = f.readlines()
		header = data.pop(0)
		data.sort(key=user_id_and_time)
		data.insert(0,header)
		return data

for line in sort(IN_FILE):
	print line.rstrip()