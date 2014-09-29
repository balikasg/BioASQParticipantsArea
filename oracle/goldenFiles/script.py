import json
for i in range(2,20):
	print "Testset", i
	f=open("testset%d/pmids.txt" %i)
	f=json.loads(f.read())
	print "Annotated articles:", len(f)
	
