import sys


print ("##fileformat=VCFv4.1")
print ("##source=WiseCondor")
print ("##ALT=<ID=DEL,Description=\"Deletion>")
print ("##ALT=<ID=DUP,Description=\"Duplication\">")

print ("##INFO=<ID=END,Number=1,Type=Integer,Description=\"The end position of the variant\">")
print ("##INFO=<ID=SVLEN,Number=1,Type=Integer,Description=\"The length of the variant\">")

print ("##FORMAT=<ID=WS,Number=2,Type=Float,Description=\"WiseCondor zscore and effect size\">")
print ("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">")

write_results=False
elements=[]
sample=""
headder=""
variants=[]
for line in open(sys.argv[1]):
	if "# Test results:"  in line:
		write_results=True
	if not write_results and not line[0] == "#":
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

	if "resultfile =" in line:
		sample=line.split("/")[-1].split(".sort")[0]
		header= ("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{}".format(sample))

	if line[0] == "#" and  elements:
		print "##" +  " ".join(elements)
		elements=[]
	if not line[0] == "#" and write_results and not "z-score\teffect" in line:
		variants.append(line.strip())

print header

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
