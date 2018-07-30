import sys

def print_wisecondor(infile):
	write_results=False
	variants=[]
	for line in open(infile):
		if "# Test results:"  in line:
			write_results=True
		if not line[0] == "#" and write_results and not "z-score\teffect" in line:
			variants.append(line.strip())

	i=0
	for variant in variants:
		content=variant.split("\t")
		zscore=content[0]
		effect=content[1]
		id=i
		if float(effect) < 0:
			ALT="DEL"
		else:
			ALT="DUP"
		qual=zscore
		filt="PASS"
		pos=float(content[-1].split(":")[-1].split("-")[0])
		chrom=content[-1].split(":")[0]
		end=float(content[-1].split("-")[-1])
		length=abs(pos-end)+1

		print "{}\t{}\tWiseCondor_{}\tN\t<{}>\t{}\tPASS\tEND={};SVLEN={};SVTYPE={}\tGT:WS\t./1:{},{}".format(chrom,int(pos),id,ALT,zscore,int(end),int(length),ALT,effect,zscore)
		i+=1

def print_ichor(infile):
	first=True
	i=0
	for line in open(infile):
		if first:
			first=False
			continue
		content=line.strip().split("\t")

		chrom = content[1]
		pos=content[2]
		end=content[3]
		length=abs(int(end)-int(pos))+1
		cn=content[6]
		if  int(cn) == 2:
			continue
		elif int(cn) < 2:
			ALT="DEL"
		elif int(cn) > 2:
			ALT="DUP"
		id=i
		i+=1

		print "{}\t{}\tichor_{}\tN\t<{}>\t.\tPASS\tEND={};SVLEN={};SVTYPE={}\tGT:CN:IC\t./1:{}:{},{}".format(chrom,int(pos),id,ALT,int(end),int(length),ALT,cn,content[5],content[6])


print ("##fileformat=VCFv4.1")
print ("##source=WiseCondor")
print ("##ALT=<ID=DEL,Description=\"Deletion>")
print ("##ALT=<ID=DUP,Description=\"Duplication\">")

print ("##INFO=<ID=END,Number=1,Type=Integer,Description=\"The end position of the variant\">")
print ("##INFO=<ID=SVLEN,Number=1,Type=Integer,Description=\"The length of the variant\">")
print ("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">")

wisecondor=False
ichor=False

condor_file=""
ichor_file=""

if len(sys.argv) == 2 or len(sys.argv) == 3:
	for infile in sys.argv[1:]:
		if infile.endswith("report.txt"):
			print ("##FORMAT=<ID=WS,Number=2,Type=Float,Description=\"WiseCondor zscore and effect size\">")
			wisecondor=True
			condor_file=infile
		elif infile.endswith(".seg.txt"):
			print ("##FORMAT=<ID=IC,Number=2,Type=Float,Description=\"Ichor median signal and subclone status\">")
			print ("##FORMAT=<ID=CN,Number=1,Type=Integer,Description=\"copy number predicted by Ichor\">")
			ichor_file=infile
			ichor=True
		else:
			print "Invalid file format: only ichor seg.txt or wisecondor report.txt allowed" 
			quit()

	if wisecondor:
		elements=[]
		for line in open(condor_file):
			if "# Test results:"  in line:
				break
			if not line[0] == "#":
				tmp=""
				if "=" in line:
					content=line.strip().split("=")
					tmp+=content[0].strip().replace(" ","_")
					tmp+="="
					tmp+="\""+content[1].strip(" ")+"\""
				elif ":" in line:
					content=line.strip().split(":")
					tmp+=content[0].strip().replace(" ","_")
					tmp+=":"
					tmp+="\""+content[1].strip(" ").strip("\t")+"\""

				if not tmp == "":
					elements.append(tmp)

			if line[0] == "#" and  elements:
				print "##" +  " ".join(elements)
				elements=[]

			if "resultfile =" in line:
				sample=line.split("/")[-1].split(".sort")[0]
				header= ("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{}".format(sample))
	elif ichor:
		first=True
		for line in open(ichor_file):
			if first:
				first=False
				continue
			content=line.strip().split()
			header= ("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{}".format(content[0]))			
			break
			

	print(header)
	if wisecondor:
		print_wisecondor(condor_file)

	if ichor:
		print_ichor(ichor_file)
else:
	print "invalid number of input files!"
	print "input either one wisecondor text file, one ichor seg.txt or both for one sample"

