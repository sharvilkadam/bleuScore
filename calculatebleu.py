import sys
import codecs
import os
import math
import operator


def readCandidate( file1 ):
    fo = codecs.open(file1, "r",encoding='utf8')
    candidate=fo.readlines()
    fo.close()
    return candidate

def readReference( path ):
    references = []
    if os.path.isfile( path ):
        rf = codecs.open(path, "r",encoding='utf8')
        references.append(rf.readlines())
        rf.close()
    else:
        for root, dirs, files in os.walk( path ):
            for f in files:
                rf = codecs.open(os.path.join(root, f), "r",encoding='utf8')
                references.append(rf.readlines())
                rf.close()
    return references

def writeBleu( str ):
    wo = codecs.open("bleu_out.txt",'w',encoding="utf8")
    wo.write(str)
    wo.close()
    return

def calculateBleu(candidate,references):
	pres=[]
	count = 0
	bp = 1
	while (count < 4):
		count+=1
		p,bp=ngram(candidate,references,count)
		#print p
		pres.append(p)
	geomMean = (reduce(operator.mul, pres)) ** (1.0 / len(pres))
	#print "BP=" + str(bp)
	bleu = geomMean * bp
	return bleu

def ngram(can,ref,n):
	count = 0
	countClip = 0
	r = 0
	c = 0
	wc = 0
	while (wc < len(can)):		#wc == si

		#for cadidaetes
		cline = can[wc]
		cdict = {}
		words = cline.strip().split()
		cnoofngrams = len(words) - n + 1
		#loop thru ngrams and add to the cdict
		wc1 = 0
		while (wc1 < cnoofngrams):
			ngram = ' '.join(words[wc1:wc1+n]).lower()
			if ngram in cdict:
				cdict[ngram] += 1
			else:
				cdict[ngram] = 1
			wc1 += 1
	   	
	   	#for references
		rlist = []
		rlenghts = []	#for brevity penalty
	    
		wc2 = 0
		while (wc2 < len(ref)):
			rlines = ref[wc2]
			rline = rlines[wc]
			rdict = {}
			rwords = rline.strip().split()
			rlenghts.append(len(rwords))
			rnoofngrams = len(rwords) - n + 1
			#loop thru ngrams and add to the rdict
			wc3 = 0
			while (wc3 < rnoofngrams):
			    ngram = ' '.join(rwords[wc3:wc3+n]).lower()
			    if ngram in rdict.keys():
			        rdict[ngram] += 1
			    else:
			        rdict[ngram] = 1
			    wc3 += 1
			rlist.append(rdict)
			wc2 += 1
	    
	    
		countClip += countClipped(cdict, rlist)
		#print cdict
		count += cnoofngrams


		c += len(words)
		#best match for lenght for brevity
		least = abs(len(words) - rlenghts[0])
		blen = rlenghts[0]
		for rl in rlenghts:
		    if abs(len(words) - rl) < least:
		        least = abs(len(words) - rl)
		        blen = rl
		r += blen
		wc += 1 #increment outer loop

	#print "CountClip:" +str(countClip) + "  Count: "+str(count)
	bp = brevity(c,r)
	if countClip == 0:
		pres = 0
	else:
		pres = float(countClip) / float(count)
	return pres,bp

def countClipped(cdict, rlist):
    ccount=0
    for c in cdict.keys():
    	cm=0
        cl=cdict[c]
        for rdict in rlist:
            if c in rdict.keys():
                cm=max(cm,rdict[c])
        cl=min(cl,cm)
        ccount+=cl
    return ccount

def brevity(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/float(c)))
    return bp



cpath = str(sys.argv[1]) #candidate data
rpath = str(sys.argv[2]) #references data
candidate = readCandidate(cpath)
references = readReference(rpath)
#print references
bleu_score = calculateBleu(candidate,references)
#print bleu_score
writeBleu(str(bleu_score))  