import sys 

import smtplib
from email.mime.text import MIMEText
mes="Testingf"
msg = MIMEText("ela gamoto")
me="geompalik@hotmail.com"
msg['Subject'] = 'The contents'
msg['From'] = me
msg['To'] = me

me="geompalik@hotmail.com"
s=smtplib.SMTP('localhost')
s.sendmail(me, [me], msg.as_string())
s.quit()





def eval1a(g, test):
        #return ("Ok",[1,1,1,1,0,0,0,0,0,0],[1,1,0,0,0,0])
        mes=[]
        if test.is_oracle== False:
                mes.append("The test set %d is not available for use in the oracle yet." %(test.test_id-1))
                return (mes, [], [])
        try:    
                len(g["documents"])
                g['documents'][0]['pmid']
                len(g['documents'][0]['labels'])
        except: 
                mes.append("Error decoding the fields of the JSON you submitted.\nAlthough it is a valid JSON object, it seems there is a problems with the names of the fields.\n Notice that the names of the fields for the JSON of Task 1A are: 'documents', 'labels' and 'pmid'.")
                return (mes, [], [])
        if not len(g['documents']) == int(test.number_of_abstracts_oracle):
                mes.append("Different number of documents between the official test set and the JSON you submitted.\nThe official test set %d contains %d articles. Your JSON contains %d." %(test.test_id-1, test.number_of_abstracts_oracle, len(g['documents'])))
                return (mes, [], [])
        lines=open('/home/bioasq/public_html/webexample/name_id_mapping.txt', 'r').read().splitlines()
        c=dict(line.split('=') for line in lines)

        pmid_list=json.loads(open('/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/pmids.txt' %test.test_id).read())
        #After having the golden, try for each system.. 
        f=open("/home/bioasq/public_html/webexample/oracle/temp/system_A_results.txt", 'w')
        myfile=File(f)
        string=""
        mes.append("Annotated documents: %d out of %d." %(len(pmid_list), test.number_of_abstracts_oracle))
        for i in range(len(pmid_list)):
                q=[element for element in g['documents'] if int(element['pmid'])==int(pmid_list[i])][0]
                string=""
                for k in range(len(q['labels'])):
                        if q['labels'][k] in c.values():
                                string+=q['labels'][k]
                                string+=" "
                if string=="":
                        string+="D005260"
                print>>myfile, string
        myfile.close()
        subprocess.call(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "converters.MapMeshResults", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mapping.txt", "/home/bioasq/public_html/webexample/oracle/temp/system_A_results.txt", "/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt"])   
                                #I need to run for the flat measures
        result=subprocess.Popen(["java", "-Xmx10G", "-cp", "$CLASSPATH:/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/flat/BioASQEvaluation.jar", "evaluation.Evaluator", "/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/golden_labels.txt" %test.test_id, "/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt"], stdout=subprocess.PIPE)
        p=result.communicate() 
        arr=p[0].split()
	result=subprocess.Popen(["/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/hierarchical/bin/HEMKit", "/home/bioasq/public_html/webexample/EvalMeasuresBioASQ/mesh/mesh_hier_int.txt", "/home/bioasq/public_html/webexample/oracle/goldenFiles/testset%d/golden_labels.txt" %test.test_id, "/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt", "1", "1"], stdout=subprocess.PIPE)
        s=result.communicate() 
        w=s[0].split()          
        os.remove("/home/bioasq/public_html/webexample/oracle/temp/system_results_mapped.txt")
        os.remove("/home/bioasq/public_html/webexample/oracle/temp/system_A_results.txt")               
        return (mes, arr, w)
