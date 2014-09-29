#!/usr/bin/python

import sys, os, subprocess, json
def rouge(gold_results, system_results):
	with open('/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/log1', 'w') as out:
		json.dump(["I exist "], out, indent=2)
        os.environ['ROUGE_EVAL_HOME']="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/data"
        os.environ['PERL5LIB']="/home/bioasq/perl5/lib/perl5"
	os.environ['PYTHONPATH']='/home/bioasq/packages/lib/python2.7/site-packages/'
        d=json.loads(open(system_results).read())
        g=json.loads(open(gold_results).read())
        i=1
        string='<ROUGE-EVAL version="1.0">\n'
        for question in d['questions']:
                string+='<EVAL ID="{0}">\n<PEER-ROOT>\n/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq\n</PEER-ROOT>\n<MODEL-ROOT>\n/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq\n</MODEL-ROOT>\n<INPUT-FORMAT TYPE="SEE">\n</INPUT-FORMAT>\n<PEERS>\n<P ID="1">system{0}.html</P>\n</PEERS>\n<MODELS>\n<M ID="A">golden{0}.html</M>\n</MODELS>\n</EVAL>\n'.format(i)
                string_system='<html>\n<head>\n<title>system</title>\n</head>\n<body bgcolor="white">\n<a name="1">[1]</a> <a href="#1" id=1>{0}</body>\n</html>'.format(question['ideal_answer'].encode('ascii', 'ignore'))
                pt="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq/system%d.html" %i
                with open(pt, 'w') as out:
			os.chmod(pt, 0o777)
                        out.write(string_system)
                i+=1
        string+="</ROUGE-EVAL>"
        pt="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq/bioasq-test.xml"
        with open(pt, 'w') as out:
		os.chmod(pt, 0o777)
                out.write(string)
        i=1
        for question in g['questions']:
                string_golden='<html>\n<head>\n<title>golden</title>\n</head>\n<body bgcolor="white">\n<a name="1">[1]</a> <a href="#1" id=1>{0}</body>\n</html>'.format(question['ideal_answer'].encode('ascii','ignore'))
                pt="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq/golden%d.html" %i
                with open(pt, 'w') as out:
			os.chmod(pt, 0o777)
                        out.write(string_golden)
                i+=1
        command="perl /home/bioasq/public_html/webexample/task1bb/rouge-bioasq/ROUGE-1.5.5.pl -c 95 -2 4 -u -x -n 4 /home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq/bioasq-test.xml 1"
        result=subprocess.Popen(command.split(),  stdout=subprocess.PIPE)
        p=result.communicate()
	a=[float(x) for x in p[0].split()]
	
	print a
        with open('/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/log', 'w') as out:
                json.dump(p, out, indent=2)
        #os.remove("/home/bioasq/public_html/webexample/bioasq-test.xml")
       	path_to_delete="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq"
        for f in os.listdir(path_to_delete):
               os.remove(os.path.join(path_to_delete,f))
        return a
rouge(sys.argv[1], sys.argv[2])

