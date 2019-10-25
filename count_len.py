import os
import argparse
import gzip

class Count:
	def __init__(self,file):
		self.file=file
		self.num=0
	def gzip_open(self):
		if self.file.endswith('.gz'):
			f_handle=gzip.open(self.file,'rb')
		else:
			f_handle=open(self.file,'r')
		return f_handle
		

	def count_gc_len(self):
		f_handle=self.gzip_open()
		len_gc=[]
		len_seq={}
		n=0
		for line in f_handle.readlines():
			n+=1
			if n%4==2:
				seq=line.strip().upper()
				len_gc.append(sum(seq.count(x) for x in ['G','C','g','c','S','s']))
				
				if len(seq) in len_seq:
					len_seq[len(seq)]+=1
				else:
					len_seq[len(seq)]=1
				
		return len_seq,len_gc
	'''
	def echo_name(self):
		print self.file
	'''
	def gc_content(self):
		len_seq,len_gc=self.count_gc_len()
		nucs=0
		for k,v in len_seq.items():
			nucs+=k*v
			
		return len_seq,float(sum(len_gc)*100/nucs)

if __name__=="__main__":
	
	parser=argparse.ArgumentParser(description="the application description")

	parser.add_argument('-f','--input',type=str,help="the input file path or file name")
	parser.add_argument('-o','--output',type=str,help="the outfile name for writing the result")

	args=parser.parse_args()

	file=args.input
	output=args.output
	if os.path.exists(file):
		print "continue"
	else:
		print "the inuput file is not exists"
	if os.path.exists(output):
		print "the outfile is exists and the results will appending the end of the file"
	else:
		print "the outfile is not exists and will make a file"

		
	fqcount=Count(file)
	len_seq,gc=fqcount.gc_content()
	with open(output,'a+') as OUT:
		i=0
		for k,v in len_seq.items():
			i+=1	
			OUT.write("%d %s sequence lenght %d: the number of this lenght is %d\t"%(i,args.input,k,v))
		OUT.write("the %s GC content is %f\n"%(args.input,gc))
	OUT.close()
