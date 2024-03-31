import re
import stanza
import getopt
import sys

try:
    stanza.download('en', confirm_if_exists=True)
    print("English models are already downloaded.")
except Exception as e:
    print("English models not found. Downloading now...")
    stanza.download('en')
    print("English models downloaded successfully.")

pronoun=["i","you","he","she","it","they","me","him","her","it","my","mine","your","yours","his","her","hers","its","who","whom","whose","what","which","another", "each","everything","nobody","either","someone","that","myself","yourself","himself","herself","itself","this"]

def extract_ner(src_text_file):
	outfile_name=re.sub(r"[.](txt)","_NER.txt",src_text_file)
	nerFile=open(outfile_name,"w")
	filename=open(src_text_file,'r')
	allData=""
	for data in filename:
		allData=allData+data
	allData=re.sub(r"(\s)*\n(\n)*(\s)*","\n",allData)
	allData=re.sub(r"(\.)*\n",".\n",allData)
	nlp = stanza.Pipeline('en', processors='tokenize,ner')
	doc = nlp(allData)
	nerCollector=[]
	for sent in doc.sentences:
		for ent in sent.ents:
			if(ent.type=="ORG" or ent.type=="PERSON" or ent.type=="GPE"):
				nerdata=ent.text
				nerdata=(nerdata.lower()).strip()
				callen=nerdata.split(" ")
				if(len(callen)>1):
					if(nerdata not in nerCollector and nerdata not in pronoun):
						nerCollector.append(nerdata)
	
	for ners in nerCollector:
		nerFile.write(ners)
		nerFile.write("\n")


def start():
	src_text_file=''
	try:
		options, remainder = getopt.getopt(sys.argv[1:], 'hi:',['ifile=', 'help'])
	except getopt.GetoptError:
		print ('nerExtract.py [-h] -i <inputfile> ')
		sys.exit(0)

	for opt, arg in options:
		if opt in ('-h', '--help'):
			print("Usage: \
				\n -i --input file, \
				\n -h, --help")
			print('command: \
			\n python3 nerExtract.py -i <inputfile>')
			sys.exit(1)
		elif opt in ('-i', '--ifile'):
			src_text_file = arg
	if(src_text_file ==""):
		print("Please use this command 'python3 nerExtract.py -i <inputfile>'")
		sys.exit(1)
	extract_ner(src_text_file)

start()