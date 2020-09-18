import sys

record = sys.argv[1]
with open(record, "r") as rrfile:
	prev = 0
	squared_sum = 0
	i = 0
	for rr in rrfile:
		i = i + 1
		if(i == 1 or rr == ""):
			prev = float(rr)
			continue
		term = prev - float(rr)
		squared_sum = squared_sum + (term*term)
		prev = float(rr)
	rmssd_squared = squared_sum/i
	sid = record.split(".")[0]
	with open("sid_rmssd.csv", "a") as finalfile:
		print(sid+","+str(rmssd_squared), end="\n", file=finalfile)
