from os import listdir

def rouge(gold_results, system_results):
        import os
        import json
        import subprocess
        os.environ['ROUGE_EVAL_HOME']="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/data"
        os.environ['PERL5LIB']="/home/bioasq/perl5/lib/perl5"
        d=json.loads(open(system_results).read())
        g=json.loads(open(gold_results).read())
        i=1
        string='<ROUGE-EVAL version="1.0">\n'
        for question in d['questions']:
                string+='<EVAL ID="{0}">\n<PEER-ROOT>\n/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq\n</PEER-ROOT>\n<MODEL-ROOT>\n/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq\n</MODEL-ROOT>\n<INPUT-FORMAT TYPE="SEE">\n</INPUT-FORMAT>\n<PEERS>\n<P ID="1">system{0}.html</P>\n</PEERS>\n<MODELS>\n<M ID="A">golden{0}.html</M>\n</MODELS>\n</EVAL>\n'.format(i)
                string_system='<html>\n<head>\n<title>system</title>\n</head>\n<body bgcolor="white">\n<a name="1">[1]</a> <a href="#1" id=1>{0}</body>\n</html>'.format(question['ideal_answer'])
                pt="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq/system%d.html" %i
                with open(pt, 'w') as out:
                        out.write(string_system)
                i+=1
        string+="</ROUGE-EVAL>"
        #print string
        pt="/home/bioasq/public_html/webexample/bioasq-test.xml"
        with open(pt, 'w') as out:
                out.write(string)
        i=1
        for question in g['questions']:
                string_golden='<html>\n<head>\n<title>golden</title>\n</head>\n<body bgcolor="white">\n<a name="1">[1]</a> <a href="#1" id=1>{0}</body>\n</html>'.format(question['ideal_answer'])
                pt="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq/golden%d.html" %i
                with open(pt, 'w') as out:
                        out.write(string_golden)
                i+=1
        command="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/ROUGE-1.5.5.pl -c 95 -2 4 -u -x -n 4 bioasq-test.xml 1"
        result=subprocess.check_output(command.split(),  stderr=subprocess.STDOUT)
        #p=result.communicate()
        #a=p[0].split()
        os.remove("/home/bioasq/public_html/webexample/bioasq-test.xml")
        path_to_delete="/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq"
        for f in listdir(path_to_delete):
               os.remove(os.path.join(path_to_delete,f))
        with open("/home/bioasq/public_html/webexample/task1bb/rouge-bioasq/bioasq/ss.txt", 'w') as out:
                out.write(result)

        return result
