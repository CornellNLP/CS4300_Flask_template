import os, pickle, json

f = open(os.getcwd() + '/Parsed JSONs/RC_2016-01.json', 'rb')
data = json.loads(f.read())
bodies = [(datum['body'] + "ENDOFLINE").encode('ascii', 'replace') for datum in data]


with open('comments.csv','w') as file_out:
	for body in bodies:
		file_out.write(body)