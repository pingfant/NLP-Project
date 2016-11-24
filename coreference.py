

from __future__ import division  
from sklearn import tree
import nltk
import os,sys


#nltk.download()


filelist=sys.argv[1]
direct=sys.argv[2]



input_file_list=[]
output_file_list=[]


file = open(filelist)
while 1:
    line = file.readline()
    if not line:
        break
    line=line.strip("\n")
    line=line.strip(" ")
    if len(line)>0:
        input_file_list.append(line)


for item in input_file_list:
    temp=item.split("/")
    name=temp[len(temp)-1]
    name=name.split(".")
    name1=name[0]
    if direct[len(direct)-1]!="/":
        name1="/"+name1
    out_name=direct+name1+".response"
    output_file_list.append(out_name)

#print input_file_list
#print output_file_list




#################################################### define some functions and constants ##################################
###########################################################################################################################


def edit_distance(str1, str2):
      len_str1 = len(str1) + 1
      len_str2 = len(str2) + 1
      #create matrix
      matrix = [0 for n in range(len_str1 * len_str2)]
      #init x axis
      for i in range(len_str1):
          matrix[i] = i
      #init y axis
      for j in range(0, len(matrix), len_str1):
          if j % len_str1 == 0:
              matrix[j] = j // len_str1

      for i in range(1, len_str1):
          for j in range(1, len_str2):
              if str1[i-1] == str2[j-1]:
                  cost = 0
              else:
                  cost = 1
              matrix[j*len_str1+i] = min(matrix[(j-1)*len_str1+i]+1,
                                          matrix[j*len_str1+(i-1)]+1,
                                          matrix[(j-1)*len_str1+(i-1)] + cost)

      return matrix[-1]


male=["he", "him",  "himself","his" ,"He", "Him",  "Himself","His"  ]
female=["her", "hers", "herself" , "she",  "Her", "Hers", "Herself" , "She"]
neutral=[ "I", "it","its", "itself",  "me", "mine","my" ,"myself", "oneself" ,"our" ,"ours", "ourselves","their", "theirs","them" ,"themselves" ,"they", "us", "we" ,"you", "your", "yours" ,"yourself" ,"yourselves",
"It","Its", "Itself",  "Me", "Mine","My" ,"Myself", "Oneself" ,"Our" ,"Ours", "Ourselves","Their", "Theirs","Them" ,"Themselves" ,"They", "Us", "We" ,"You", "Your", "Yours" ,"Yourself" ,"Yourselves"]



singular=["he", "her" ,"she" ,"hers", "herself" , "him", "himself" ,"his", "I", "it", "its" ,"itself","me", "mine" ,"my" ,"myself" ,"yourself",
"He", "Her" ,"She" ,"Hers", "Herself" , "Him", "Himself" ,"His","It", "Its" ,"Itself","Me", "Mine" ,"My" ,"Myself" ,"Yourself"]
plural=[ "oneself","our", "ours" ,"ourselves", "their" ,"theirs", "them" ,"themselves","they" ,"us" ,"we" ,"yourselves",
"Oneself","Our", "Ours" ,"Ourselves", "Their" ,"Theirs", "Them" ,"Themselves","They" ,"Us" ,"We" ,"Yourselves" ]
uncertain=["you" ,"your" ,"yours","You" ,"Your" ,"Yours"]



person1=[ "I","me", "mine" ,"my" ,"myself" ,"our" ,"ours" ,"ourselves"  , "us" ,"we",
 "Me", "Mine" ,"My" ,"Myself" ,"Our" ,"Ours" ,"Ourselves"  , "Us" ,"We"]
person2=[ "you", "your", "yours", "yourself", "yourselves","You", "Your", "Yours", "Yourself", "Yourselves"]
person3=["he", "her",  "hers" ,"herself" , "him" ,"himself" ,"his", "it" ,"its" ,"itself" ,"she" ,"their" ,"theirs" ,"them" ,"themselves" ,"they",
"He", "Her",  "Hers" ,"Herself" , "Him" ,"Himself" ,"His", "It" ,"Its" ,"Itself" ,"She" ,"Their" ,"Theirs" ,"Them" ,"Themselves" ,"They"]
person0=["oneself", "Oneself"]

verb=["VB", "VBD", "VBG","VBN","VBP","VBZ"]

pronoun=["PRP","PRP$"]
noun=["NN","NNS","NNP","NNPS"]


time=["day","days","Day","Days","week","weeks","Week","Weeks",
"month", "months","Month", "Months","year","years","Year","Years","today","Today", "yesterday","Yesterday",
"tomorrow","Tomorrow","decade","decades","Decade","Decades","time",
"Monday", "Tuesday","Wedesday","Thursday","Friday","Saturday","Sunday", 
"January", "Jan.", "February", "Feb.", "Marcy", "Mar.","April", "Apr.", "May", "June", "Jun.", "July", "Jul.", "August", "Aug.", "September", "Sep.","Sept.",  "October", "Oct.", "November", "Nov.", "December","Dec.", "number","value","amount","quantity","sum"]

det=["a","the"]
prepo=["at", "in", "on", "by" "for", "under" "since", "to", "toward", "from", "of", "before", "after", "behind","up","down","about"]


'''
NN     Noun, singular or mass 
NNS     Noun, plural 
NNP     Proper noun, singular
NNPS     Proper noun, plural 
'''

'''
  CD     Cardinal number  
  JJ     Adjective
'''

'''
PRP     Personal pronoun
PRP$     Possessive pronoun
'''

#################################################################################################################################
#################################################################################################################################







#################################################### begin train ###############################################################
################################################################################################################################


file_list=["a8.fkey","a9.fkey","a10.fkey","a11.fkey","a12.fkey","b1.fkey","b2.fkey","b3.fkey","b4.fkey","b5.fkey","b6.fkey",
"b7.fkey","b8.fkey","b9.fkey","b10.fkey"]


train_data=[]
train_label=[]


for file_name in file_list:

        print "processing "+file_name
	file = open(file_name)
	temp_file=file.read()
	temp_file_1=temp_file.strip("\n")
	temp_file_1=temp_file_1.strip("<TXT>")
	temp_file_1=temp_file_1.strip("</TXT>")
	temp_file_1=temp_file_1.replace("\n\n",".\n\n ")
	temp_file_1=temp_file_1.replace("..\n\n",".\n\n ")



	sent=nltk.sent_tokenize(temp_file_1)

	word=[]

	i=1
	j0=0
	ID=""
	ref=""

	for item in sent:
		#print "----------------------------- this is one sentence ------------------------"
		#print i
		#item=sent[0]
		item=item.replace("\n"," ")
		item=item.replace("<COREF ID=\""," AAACOREFID=")
		item=item.replace("\">","ATAAA")
		item=item.replace("\" REF=\"","REF=")
		item=item.replace("</COREF>","AAA/COREFAAA ")

		s_number=i
		i=i+1;

		#print "****************************************\n\n"
		#print item
		#print "****************************************\n\n"

		text = nltk.word_tokenize(item)

		#print text


		len_text=len(text)
		text1=[]


		start1=0

		for j in range(0,len_text):
		    start1=text[j].find("AAACOREFID")
		    start2=text[j].find("AAA/COREFAAA")

		    if start1 !=-1:
			start1=text[j].find("ATAAA")+5
			end=text[j].find("AAA/COREFAAA")
			if end !=-1:
			    text1.append(text[j][start1:end])
			else:
			    text1.append(text[j][start1:len(text[j])])

		    elif start2 !=-1:
			text1.append(text[j][0:start2])
		    else:
			text1.append(text[j])

		#print "***************************** \n \n"     
		#print text1

		tag=nltk.pos_tag(text1)
		left=0

		for j in range(0,len_text):
		    start1=text[j].find("AAACOREFID")
		    start2=text[j].find("AAA/COREFAAA")
		    temp={}
		    if start1 !=-1:
			left=j
			ID_left=text[j].find("ID=")+3
			ID_right=text[j].find("REF=")
			if ID_right==-1:
			    ID_right=text[j].find("ATAAA")
		            ref="AAA"
		        else:
			    ref_left=ID_right+4
		            ref_right=text[j].find("ATAAA")
		            ref=text[j][ref_left:ref_right]

			ID=text[j][ID_left:ID_right]
			end=text[j].find("AAA/COREFAAA")
			if end !=-1:
			    right=j
			    name=text1[j]
			    temp["name"]=name
			    temp["begin"]=left
			    temp["end"]=right
			    temp["s_number"]=s_number
			    temp["id"]=j0
			    j0=j0+1
			    temp["ID"]=ID
		            temp["ref"]=ref

		            # gender
		            # unknown 0
		            # male 1
		            # female -1
		            # neither male nor female 2

			    if tag[j][1] in pronoun:
		                if text1[j] in male:
		                    temp["gender"]=1
		                elif text1[j] in female:
		                    temp["gender"]=-1
		                elif text1[j] in neutral:
		                    temp["gender"]=2
		                else:
		                    temp["gender"]=0
		            else:
		                temp["gender"]=0


		            # number
		            # unkonwn 0
		            # singular 1
		            # plural -1
		        

			    if tag[j][1] in pronoun:
		                if text1[j] in singular:
		                    temp["number"]=1
		                elif text1[j] in plural:
		                    temp["number"]=-1
		                else:
		                    temp["number"]=0

			    elif tag[j][1]=="NN" or tag[j][1]=="NNP":
		                temp["number"]=1
			    elif tag[j][1] =="NNS" or tag[j][1]=="NNPS":
		                temp["number"]=-1
		            else:
		                temp["number"]=0


			    if tag[j][1] in pronoun:
		                if text1[j] in person1:
		                    temp["person"]=1
		                elif text1[j] in person2:
		                    temp["person"]=2
				elif text1[j] in person3:
		                    temp["person"]=3
		                else:
		                    temp["person"]=0
		            else:
		                temp["person"]=0

		            # unknown 0
		            # proper 1
		            # noun 2
		            # pronoun 3
		            # time or number 4

		     
		
		            if tag[j][1]=="NNP" or tag[j][1]=="NNPS":
		                temp["l_form"]=1
		            elif tag[j][1]=="NN" or tag[j][1]=="NNS":
		                temp["l_form"]=2
		            elif tag[j][1] in pronoun:
		                temp["l_form"]=3
		            elif tag[j][1]=="CD" or text1[j] in time:
				temp["l_form"]=4
		            else:
		                temp["l_form"]=0
		           

		            # unknow 0
		            # subject 1
		            # object 2
		            # PP 3
		          
		            flag_grole=0

		            k=j

		            while k<len(tag) and j-k<=3:
				if tag[k][1]=="IN":
				    temp["g_role"]=3
				    flag_grole=1
				    break
				else:
				    k=k-1

			    if flag_grole==0:
		                k=j
				while k<len(tag) and k>=0 and j-k<=3:
				    if tag[k][1] in verb:
				        temp["g_role"]=2
				        flag_grole=1
				        break
				    else:
					k=k-1
			    if flag_grole==0:
		                k=j
				while k<len(tag) and k>=0 and k-j<=3:
		                    if tag[k][1] in verb:
		                        temp["g_role"]=1
		                        flag_grole=1
		                        break
				    else:
					k=k+1

			    if flag_grole==0:
		                  temp["g_role"]=0

			    word.append(temp)


		    elif start2 !=-1:
			right=j
			name=""
			for k in range(left,right+1):
			    name=name+text1[k]+" "
			name=name.strip(" ")
			temp["name"]=name
			temp["begin"]=left
			temp["end"]=right
			temp["s_number"]=s_number
			temp["id"]=j0
			j0=j0+1
			temp["ID"]=ID
		        temp["ref"]=ref
			temp["gender"]=0
		        if tag[right][1]=="NN" or tag[right][1]=="NNP":
		                temp["number"]=1
			elif tag[right][1] =="NNS" or tag[right][1]=="NNPS":
		                temp["number"]=-1
		        else:
		                temp["number"]=0

		        temp["person"]=0
		        ############################################################
		        flag_lform=0
		        for k in range(left,right+1):
		            if tag[k][1]=="NNP" or tag[k][1]=="NNPS":
		                temp["l_form"]=1
		                flag_lform=1
		                break
		        if flag_lform==0:
		            for k in range(left,right+1):
		                if text1[k] in time and (right-left+1)<=3:
		                    temp["l_form"]=4
		                    flag_lform=1
		                    break
		        if flag_lform==0:
		            for k in range(left,right+1):
		                if tag[k][1]!="CD":
		                    flag_lform=2
		                    break
		            if flag_lform==0:
		                temp["l_form"]=4
		                flag_lform=1

		        if flag_lform==2:
		            temp["l_form"]=2
		        ############################################################

		        flag_grole=0
		        k=right
		        while k<len(tag) and k>=0 and k-right<=3:
		            if tag[k][1] in verb:
		                temp["g_role"]=1
		                flag_grole=1
		                break
			    else:
				k=k+1
			if flag_grole==0:
		            k=left
			    while k<len(tag) and k>=0 and left-k<=3:
			        if tag[k][1] in verb:
			            temp["g_role"]=2
			            flag_grole=1
			            break
				else:
				    k=k-1
			if flag_grole==0:
		            k=right
			    while k<len(tag)and k>=0 and k-right<=3:
			        if tag[k][1]=="IN":
			            temp["g_role"]=3
			            flag_grole=1
			            break
				else:
				    k=k+1
		        if flag_grole==0:
		            temp["g_role"]=0

			word.append(temp)



	#print "\n \n ----------------- the item in word ----------- \n \n "
	'''
	for item in word:
	    print item
	    #print item["name"]+"  ******  "+str(item["l_form"])
	'''
	#print len(sent)



	vector=[]
	label=[]
	index={}

	for  i in range(0,len(word)):
	    index[word[i]["ID"]]=word[i]["id"]
	#print index

	for i in range(len(word)-1,-1,-1):
	  
	    if word[i]["ref"]!="AAA":
		pair={}
		end=index[word[i]["ref"]]
		#pair["label"]=1
		label.append(1)

		#pair["anaphor"]=word[i]["ID"]
		#pair["antecedent"]=word[end]["ID"]

		if word[i]["gender"]*word[end]["gender"]==1 or  word[i]["gender"]*word[end]["gender"]==4:
		    pair["strict_gender"]=1
		    pair["compatible_gender"]=1
		elif word[i]["gender"]*word[end]["gender"]==0:
		    pair["strict_gender"]=0
		    pair["compatible_gender"]=1
		else:
		    pair["strict_gender"]=0
		    pair["compatible_gender"]=0

		if word[i]["number"]*word[end]["number"]==1:
		    pair["strict_number"]=1
		    pair["compatible_number"]=1
		elif word[i]["number"]*word[end]["number"]==-1:
		    pair["strict_number"]=0
		    pair["compatible_number"]=0
		else:
		    pair["strict_number"]=0
		    pair["compatible_number"]=1

		pair["s_distance"]=abs( word[i]["s_number"]-word[end]["s_number"])
		pair["h_distance"]=abs( word[i]["id"]-word[end]["id"]) 

		pair["g_role"]=word[end]["g_role"]
		pair["l_form"]=word[end]["l_form"]

		#pair["anaphor_ed"]=(len(word[end]["name"])-edit_distance(word[end]["name"],word[i]["name"]))/len(word[end]["name"])
		#pair["antecedent_ed"]=(len(word[i]["name"])-edit_distance(word[i]["name"],word[end]["name"]))/len(word[i]["name"])
	  
		e_distance=edit_distance(word[end]["name"],word[i]["name"])/max(len(word[end]["name"]), len(word[i]["name"]))
		if e_distance<=0.25:
		    pair["edit_distance"]=0
		elif e_distance>0.25 and e_distance<=0.5:
		    pair["edit_distance"]=1
		elif e_distance>0.5 and e_distance<=0.75:
		    pair["edit_distance"]=2
		else:
		    pair["edit_distance"]=3


		vector.append(pair)
		
		j=i-1
		while j>=0 and i-j<=5 and j>end:
			pair={}
			pair["label"]=0

			#pair["anaphor"]=word[i]["ID"]
			#pair["antecedent"]=word[end]["ID"]

			if word[i]["gender"]*word[j]["gender"]==1 or  word[i]["gender"]*word[j]["gender"]==4:
			    pair["strict_gender"]=1
			    pair["compatible_gender"]=1
			elif word[i]["gender"]*word[j]["gender"]==0:
			    pair["strict_gender"]=0
			    pair["compatible_gender"]=1
			else:
			    pair["strict_gender"]=0
			    pair["compatible_gender"]=0

			if word[i]["number"]*word[j]["number"]==1:
			    pair["strict_number"]=1
			    pair["compatible_number"]=1
			elif word[i]["number"]*word[j]["number"]==-1:
			    pair["strict_number"]=0
			    pair["compatible_number"]=0
			else:
			    pair["strict_number"]=0
			    pair["compatible_number"]=1

			pair["s_distance"]=abs( word[i]["s_number"]-word[j]["s_number"])
			pair["h_distance"]=abs( word[i]["id"]-word[j]["id"]) 

			pair["g_role"]=word[j]["g_role"]
			pair["l_form"]=word[j]["l_form"]
			#pair["anaphor_ed"]=(len(word[j]["name"])-edit_distance(word[j]["name"],word[i]["name"]))/len(word[j]["name"])
			#pair["antecedent_ed"]=(len(word[i]["name"])-edit_distance(word[i]["name"],word[j]["name"]))/len(word[i]["name"])
		  

		        e_distance=edit_distance(word[j]["name"],word[i]["name"])/max(len(word[j]["name"]), len(word[i]["name"]))
		        if e_distance<=0.25:
		            pair["edit_distance"]=0
		        elif e_distance>0.25 and e_distance<=0.5:
		            pair["edit_distance"]=1
		        elif e_distance>0.5 and e_distance<=0.75:
		            pair["edit_distance"]=2
		        else:
		            pair["edit_distance"]=3


		        if pair not in vector:
			    vector.append(pair)
		            label.append(0)
		        j=j-1
		    
	'''
	for i in range(0,len(vector)):
	    print vector[i]
	    print label[i]


	print len(vector)
	print len(label)
	'''


	#train_label=train_label+label

	for k in range(0,len(vector)):
            item=vector[k]
	    temp=[]
	    temp.append(item["strict_gender"])
	    temp.append(item["compatible_gender"])
	    temp.append(item["strict_number"])
	    temp.append(item["compatible_number"])
	    temp.append(item["s_distance"])
	    temp.append(item["h_distance"])
	    temp.append(item["g_role"])
	    temp.append(item["l_form"])
	    temp.append(item["edit_distance"])

            if temp not in train_data: 
	        train_data.append(temp)
                train_label.append(label[k])

	'''
	for item in train_data:
	    print item

	print len(train_data)

	positive=0

	for item in label:
	    if item==1:
		positive=positive+1

	print positive
	'''


#print len(train_data)
#print len(train_label)

positive=0
for item in train_label:
    if item==1:
	positive=positive+1

#print positive


clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_data,train_label)


#print clf.predict(train_data[0])
#print label[0]


#################################################### end train ###############################################################
##############################################################################################################################






####################################################  preprocess function ####################################################
##############################################################################################################################




def preprocess(input_name):

	pronoun=["PRP","PRP$"]
	noun=["NN","NNS","NNP","NNPS"]
        line_break=[" ","\n"]

	#file = open("a8.crf")
	file = open(input_name)
         
	temp_file=file.read()


	############################################################## function 1
        
        
	temp_file1=temp_file
	temp_file1=temp_file1.replace("<COREF ID=\"","AAACOREFID=")
	temp_file1=temp_file1.replace("\">","ATAAA")
	#temp_file1=temp_file1.replace("\" REF=\"","REF=")
	temp_file1=temp_file1.replace("</COREF>","AAA/COREFAAA")
	temp_file1=temp_file1.replace("<TXT>","AAATXTAAA")
	temp_file1=temp_file1.replace("</TXT>","EEETXTEEE")

	sent1=nltk.sent_tokenize(temp_file1)

	between_sent=[]

	i=0
	begin5=0
	end5=0
	while i<len(sent1)-1:
	    item1=sent1[i]
	    item2=sent1[i+1]
	    begin5=end5+temp_file1[end5:len(temp_file1)].find(item1)+len(item1)
	    end5=begin5+temp_file1[begin5:len(temp_file1)].find(item2)
	    between_sent.append(temp_file1[begin5:end5])
	    i=i+1

	item1=sent1[i]
	begin5=end5+temp_file1[end5:len(temp_file1)].find(item1)+len(sent1[i])
	end5=len(temp_file1)
	between_sent.append(temp_file1[begin5:end5])

	sent2=[]
	between_sent2=[]
	i=0
	while i<len(sent1):
	#while i<13:

	    #print sent1[i]
	    flag=0
	    flag1=sent1[i].find("AAACOREFID=")
	    flag2=sent1[i].find("AAA/COREFAAA")
	    #print flag1
	    #print flag2
	    if flag1==-1 and flag2==-1:
		flag=0
	    if flag1!=-1 and flag2!=-1 and flag1<flag2:
		flag=0
	    if flag1!=-1 and flag2!=-1 and flag1>flag2:
		flag=1
	    if flag1==-1 and flag2!=-1:
		flag=1
	    if flag1!=-1 and flag2==-1:
		flag=0

	    if flag==1:
		#sent2[len(sent2)-1]=sent1[i-1]+between_sent[i-1]+sent1[i]
		sent2[len(sent2)-1]=sent2[len(sent2)-1]+between_sent[i-1]+sent1[i]
		between_sent2[len(between_sent2)-1]=between_sent[i]
		i=i+1
	    else:
		sent2.append(sent1[i])
		between_sent2.append(between_sent[i])
		i=i+1


	##############################################################


	count=1

	#print len(sent)    
	#print len(sent1)


	#print len(sent1)



	split_note=[" ","\n",",",":",";"]


	sent3=[]

	for sent_item in sent2:

	    text1=[]
	    between_words=[]
	    i=0
	    begin=0
	    end=-1
	    while i<len(sent_item):
		if sent_item[i] in split_note or (sent_item[i]=="." and i==len(sent_item)-1):
		    end=i
		    temp1=sent_item[begin:end]
		    text1.append(temp1)
		    begin1=end
		    while i<len(sent_item) and (sent_item[i] in split_note or (sent_item[i]=="." and i==len(sent_item)-1)):
		        i=i+1
		    end1=i
		    begin=i
		    temp2=sent_item[begin1:end1]
		    between_words.append(temp2)
		i=i+1
	    if begin<len(sent_item) and begin>end:
	       text1.append(sent_item[begin:len(sent_item)])
	       between_words.append("")


	    #if len(text1)!=len(between_words):
	    #    print "error"
	    #    break

	    List=[]
	    text2=[]
	    for j in range(0,len(text1)):
		start1=text1[j].find("AAACOREFID")
		start2=text1[j].find("AAA/COREFAAA")
		if start1 !=-1:
		    begin1=j
		    start1=text1[j].find("ATAAA")+5
		    end=text1[j].find("AAA/COREFAAA")
		    if end !=-1:
			#end1=j
			List.append(j)
			text2.append(text1[j][start1:end])
		    else:
			text2.append(text1[j][start1:len(text1[j])])

		elif start2 !=-1:
		    end1=j
		    for k in range(begin1,end1+1):
			List.append(k)
		    text2.append(text1[j][0:start2])
		else:
		    text2.append(text1[j])

	    text3=[]
	    for item1 in text2:
		if len(item1)>5:
		    item1=item1.lower()
		text3.append(item1)
	    tag=nltk.pos_tag(text3)

	    #print tag
	    #print "-----------------------------------"

	    text5=[]

	    i=0
	    while i<len(text1):
		if text1[i]!="AAATXTAAA" and text1[i]!="EEETXTEEE" and i not in List:
		    if tag[i][1] in pronoun or tag[i][1]=="CD":
		        text1[i]="<COREF ID=\"X" +str(count)+"\">"+text1[i]+"</COREF>"
		        count=count+1
		        i=i+1
		    elif tag[i][1] in noun:
		        text1[i]="<COREF ID=\"X" +str(count)+"\">"+text1[i]
		        count=count+1
		        while i<len(text1) and tag[i][1] in noun and text1[i]!="AAATXTAAA" and text1[i]!="EEETXTEEE" and i not in List:
		            i=i+1
		        i=i-1
		        text1[i]=text1[i]+"</COREF>"
		        i=i+1
		i=i+1

	    
	    #print text1
	    #print "-----------------------------------"

	    temp_sent=""
	    for i in range(0,len(text1)):
		temp_sent=temp_sent+text1[i]+between_words[i]
	   
	    sent3.append(temp_sent)
	    

	output=""
	for i in range(0,len(sent3)):
	    output=output+sent3[i]+between_sent2[i]



	#print len(sent3)
	#print len(between_sent2)

	output=output.replace("AAACOREFID=","<COREF ID=\"")
	output=output.replace("ATAAA", "\">")
	output=output.replace("AAA/COREFAAA","</COREF>")
	output=output.replace("AAATXTAAA","<TXT>")
	output=output.replace("EEETXTEEE","</TXT>")

	return output

        
        
        #################################################################################  funvtion 2
        
        '''
	sent1=[]
	begin2=0
	end2=0

	i=0

	while i<len(temp_file):
	    if temp_file[i]=="." or  temp_file[i]=="!" or  temp_file[i]=="?":
		if i+1<len(temp_file) and temp_file[i+1] in line_break:
                   
		    flag1=temp_file[i:len(temp_file)].find("<COREF ID")
		    flag2=temp_file[i:len(temp_file)].find("</COREF>")
		    flag=0
		    if flag1==-1 and flag2==-1:
		        flag=1
		    elif flag1!=-1 and flag2!=-1 and flag1<flag2:
		        flag=1
                    elif flag1!=-1 and flag2!=-1 and flag1>=flag2:
		        flag=0
		    elif flag1==-1 and flag2!=-1:
		        flag=0

		    if flag==1:
		        end2=i
		        sent1.append(temp_file[begin2:end2+1])
		        begin2=end2+1
		        end2=begin2
	    i=i+1

	end2=len(temp_file)-1
	sent1.append(temp_file[begin2:end2+1])

        ##################################################################################



	count=1

	#print len(sent)    
	#print len(sent1)


	sent2=[]

	#print len(sent1)

	for item in sent1:

		#item=sent1[0]

		#print"\n\n\n\n\n\n"

		#print repr(item)
		#print item

		#print "***********************************************"

		text_1=item
		text_1=text_1.strip("\n")

		text_1=text_1.replace("<COREF ID=\""," AAACOREFID=")
		text_1=text_1.replace("\">","ATAAA")
		text_1=text_1.replace("\" REF=\"","REF=")
		text_1=text_1.replace("</COREF>","AAA/COREFAAA ")
		text_1=text_1.strip(" ")
		if item.find("<TXT>")!=-1:
		    text_1=text_1.strip("<TXT>")
		if item.find("</TXT>")!=-1:
		    text_1=text_1.strip("</TXT>")
		text_1=text_1.replace("\n"," ")

		#print repr(text_1)
		#print text_1

		#print "---------------------------------------------------"


		text_1=nltk.word_tokenize(text_1)
		#print text_1

		text_2=[]
		List=[]

		for j in range(0,len(text_1)):
		    start1=text_1[j].find("AAACOREFID")
		    start2=text_1[j].find("AAA/COREFAAA")

		    if start1 !=-1:
			begin1=j
			start1=text_1[j].find("ATAAA")+5
			end=text_1[j].find("AAA/COREFAAA")
			if end !=-1:
			    end1=j
			    List.append(j)
			    text_2.append(text_1[j][start1:end])
			else:
			    text_2.append(text_1[j][start1:len(text_1[j])])

		    elif start2 !=-1:
			end1=j
			for k in range(begin1,end1+1):
			    List.append(k)
			text_2.append(text_1[j][0:start2])
		    else:
			text_2.append(text_1[j])

		#print text_2

		#print List
		#print len(text_1)
		#print len(text_2)

		text_3=[]
		for item1 in text_2:
		    item1=item1.lower()
		    text_3.append(item1)

		tag=nltk.pos_tag(text_3)
		#for j in range(0,len(tag)):
		#   print tag[j]
		#   print j

		#print tag


		ref_list=[]

		j=0
		while j<len(tag):
		    temp=[]
		    if tag[j][1]=="CD" and j not in List:
			temp.append(j)
			temp.append(j)
			ref_list.append(temp)
			j=j+1
		    elif tag[j][1] in pronoun and j not in List:
		        if j+1<len(tag) and tag[j][0]=="i" and tag[j+1][0]==".":
		            j=j+1
		            continue

			temp.append(j)
			temp.append(j)
			ref_list.append(temp)
			j=j+1
		    elif tag[j][1] in noun and tag[j][0]!="(" and tag[j][0]!=")" and j not in List:
			begin=j
			end=j
			j=j+1
			while j<len(tag) and tag[j][1] in noun and j not in List:
			    end=j
			    j=j+1
			temp.append(begin)
			temp.append(end)
			ref_list.append(temp)
		    else:
			j=j+1

		#print ref_list

		begin_1=0

		for index in ref_list:

		#print "/////////////////////////////////////////////////////"
		#print item

	            if index[0]==index[1]:
		    	str1=text_2[index[0]]

			while 1:
			    begin3=begin_1+item[begin_1:len(item)].find("<COREF ID=")
			    end3=begin_1+item[begin_1:len(item)].find("</COREF>")+7        
			    pos=begin_1+item[begin_1:len(item)].find(str1)
			    if begin3+1!=begin_1 and pos>=begin3 and pos<=end3:
				begin_1=end3+1
		                #print ".................................... 0 .........................................."
				continue

		   	    part1=item[0:pos]
			    part2=item[pos:pos+len(str1)]
			    part3=item[pos+len(str1):len(item)]
			    item=part1+"<COREF ID=\"X" +str(count)+"\">"+part2+"</COREF>"+part3
			    #print item
			    #print ".................................... 1 .........................................."
			    count=count+1
			    begin_1=pos+len("<COREF ID=\"X" +str(count)+"\">"+part2+"</COREF>")
			    break


		    if index[0]!=index[1]:
			str1=text_2[index[0]]
			str2=text_2[index[1]]
			#print str1
			#print str2

			while 1:
			    begin3=begin_1+item[begin_1:len(item)].find("<COREF ID=")
			    end3=begin_1+item[begin_1:len(item)].find("</COREF>")+7   

			    pos1=begin_1+item[begin_1:len(item)].find(str1)
			    #print pos1
			    pos2=pos1+len(str1)+item[pos1+len(str1):len(item)].find(str2)
			    #print pos2

			    if begin3==begin_1-1 or end3==begin_1-1 or pos2<begin3 or end3<pos1:
				part1=item[0:pos1]
				part2=item[pos1:pos2+len(str2)]
				part3=item[pos2+len(str2):len(item)]
				item=part1+"<COREF ID=\"X" +str(count)+"\">"+part2+"</COREF>"+part3
				#print item
				#print ".................................. 2 ............................................"
				count=count+1
				begin_1=pos1+len("<COREF ID=\"X" +str(count)+"\">"+part2+"</COREF>")
				break
			    else:
				begin_1=end3+1
		                #print  ".................................. 3 ............................................"
				continue



		#print "**************************************************************"
		#print item
		sent2.append(item)


	output=""
	for item in sent2:
	    #output=output+item+"."
            output=output+item

	#output=output[0:len(output)-1]


        return output
        '''
        

##############################################################################################################################
##############################################################################################################################





#################################################### begin predict ###########################################################
##############################################################################################################################



def compare1(a,b):
    if a["prob"]<b["prob"]:
        return 1
    elif a["prob"]>b["prob"]:
        return -1
    elif a["h_distance"]>b["h_distance"]:
        return 1
    else:
        return -1


def derive_vector(word1,word2):

        # word1: antecedent
        # word2: anaphor

        pair={}
	if word1["gender"]*word2["gender"]==1 or  word1["gender"]*word2["gender"]==4:
	    pair["strict_gender"]=1
	    pair["compatible_gender"]=1
	elif word1["gender"]*word2["gender"]==0:
	    pair["strict_gender"]=0
	    pair["compatible_gender"]=1
	else:
	    pair["strict_gender"]=0
	    pair["compatible_gender"]=0

	if word1["number"]*word2["number"]==1:
	    pair["strict_number"]=1
	    pair["compatible_number"]=1
	elif word1["number"]*word2["number"]==-1:
	    pair["strict_number"]=0
	    pair["compatible_number"]=0
	else:
	    pair["strict_number"]=0
	    pair["compatible_number"]=1

	pair["s_distance"]=abs( word1["s_number"]-word2["s_number"])
	pair["h_distance"]=abs( word1["id"]-word2["id"]) 

	pair["g_role"]=word1["g_role"]
	pair["l_form"]=word1["l_form"]

	#pair["anaphor_ed"]=(len(word[end]["name"])-edit_distance(word[end]["name"],word[i]["name"]))/len(word[end]["name"])
	#pair["antecedent_ed"]=(len(word[i]["name"])-edit_distance(word[i]["name"],word[end]["name"]))/len(word[i]["name"])
  
	e_distance=edit_distance(word1["name"],word2["name"])/max(len(word1["name"]), len(word2["name"]))
	if e_distance<=0.25:
	    pair["edit_distance"]=0
	elif e_distance>0.25 and e_distance<=0.5:
	    pair["edit_distance"]=1
	elif e_distance>0.5 and e_distance<=0.75:
	    pair["edit_distance"]=2
	else:
	    pair["edit_distance"]=3

        item=pair
        temp=[]
        temp.append(item["strict_gender"])
        temp.append(item["compatible_gender"])
        temp.append(item["strict_number"])
        temp.append(item["compatible_number"])
        temp.append(item["s_distance"])
        temp.append(item["h_distance"])
        temp.append(item["g_role"])
        temp.append(item["l_form"])
        temp.append(item["edit_distance"])

        return temp




#input_file_list=["a8.crf","a9.crf"]
#output_file_list=["a8.output","a9.output"]

for h1 in range(0,len(input_file_list)):

        print "processing "+input_file_list[h1]
        preprocessed_file=preprocess(input_file_list[h1])
	temp_file=preprocessed_file
	temp_file_1=temp_file.strip("\n")
	temp_file_1=temp_file_1.strip("<TXT>")
	temp_file_1=temp_file_1.strip("</TXT>")
	temp_file_1=temp_file_1.replace("\n\n",".\n\n ")
	temp_file_1=temp_file_1.replace("..\n\n",".\n\n ")

	sent=nltk.sent_tokenize(temp_file_1)

	word=[]

	i=1
	j0=0
	ID=""


	for item in sent:
		#print "----------------------------- this is one sentence ------------------------"
		#print i
		#item=sent[0]
		item=item.replace("\n"," ")
		item=item.replace("<COREF ID=\""," AAACOREFID=")
		item=item.replace("\">","ATAAA")
		item=item.replace("</COREF>","AAA/COREFAAA ")

		s_number=i
		i=i+1;

		#print "****************************************\n\n"
		#print item
		#print "****************************************\n\n"

		text = nltk.word_tokenize(item)

		#print text


		len_text=len(text)
		text1=[]


		start1=0

		for j in range(0,len_text):
		    start1=text[j].find("AAACOREFID")
		    start2=text[j].find("AAA/COREFAAA")

		    if start1 !=-1:
			start1=text[j].find("ATAAA")+5
			end=text[j].find("AAA/COREFAAA")
			if end !=-1:
			    text1.append(text[j][start1:end])
			else:
			    text1.append(text[j][start1:len(text[j])])

		    elif start2 !=-1:
			text1.append(text[j][0:start2])
		    else:
			text1.append(text[j])

		#print "***************************** \n \n"     
		#print text1

		tag=nltk.pos_tag(text1)
		left=0



		for j in range(0,len_text):
		    start1=text[j].find("AAACOREFID")
		    start2=text[j].find("AAA/COREFAAA")
		    temp={}
		    if start1 !=-1:
			left=j
			ID_left=text[j].find("ID=")+3
		        ID_right=text[j].find("ATAAA")
			
			ID=text[j][ID_left:ID_right]
			end=text[j].find("AAA/COREFAAA")
			if end !=-1:
			    right=j
			    name=text1[j]
			    temp["name"]=name
			    temp["begin"]=left
			    temp["end"]=right
			    temp["s_number"]=s_number
			    temp["id"]=j0
			    j0=j0+1
			    temp["ID"]=ID

			    # gender
			    # unknown 0
			    # male 1
			    # female -1
			    # neither male nor female 2

			    if tag[j][1] in pronoun:
			        if text1[j] in male:
			            temp["gender"]=1
			        elif text1[j] in female:
			            temp["gender"]=-1
			        elif text1[j] in neutral:
			            temp["gender"]=2
			        else:
			            temp["gender"]=0
			    else:
			        temp["gender"]=0


			    # number
			    # unkonwn 0
			    # singular 1
			    # plural -1
			

			    if tag[j][1] in pronoun:
			        if text1[j] in singular:
			            temp["number"]=1
			        elif text1[j] in plural:
			            temp["number"]=-1
			        else:
			            temp["number"]=0

			    elif tag[j][1]=="NN" or tag[j][1]=="NNP":
			        temp["number"]=1
			    elif tag[j][1] =="NNS" or tag[j][1]=="NNPS":
			        temp["number"]=-1
			    else:
			        temp["number"]=0


			    if tag[j][1] in pronoun:
			        if text1[j] in person1:
			            temp["person"]=1
			        elif text1[j] in person2:
			            temp["person"]=2
				elif text1[j] in person3:
			            temp["person"]=3
			        else:
			            temp["person"]=0
			    else:
			        temp["person"]=0

			    # unknown 0
			    # proper 1
			    # noun 2
			    # pronoun 3
			    # time or number 4

		     
	
			    if tag[j][1]=="NNP" or tag[j][1]=="NNPS":
			        temp["l_form"]=1
			    elif tag[j][1]=="NN" or tag[j][1]=="NNS":
			        temp["l_form"]=2
			    elif tag[j][1] in pronoun:
			        temp["l_form"]=3
			    elif tag[j][1]=="CD" or text1[j] in time:
				temp["l_form"]=4
			    else:
			        temp["l_form"]=0
			   

			    # unknow 0
			    # subject 1
			    # object 2
			    # PP 3
			  
			    flag_grole=0

			    k=j

			    while k<len(tag) and k>=0 and j-k<=3:
				if tag[k][1]=="IN":
				    temp["g_role"]=3
				    flag_grole=1
				    break
				else:
				    k=k-1

			    if flag_grole==0:
			        k=j
				while k<len(tag) and k>=0 and j-k<=3:
				    if tag[k][1] in verb:
					temp["g_role"]=2
					flag_grole=1
					break
				    else:
					k=k-1
			    if flag_grole==0:
			        k=j
				while k<len(tag) and k>=0 and k-j<=3:
			            if tag[k][1] in verb:
			                temp["g_role"]=1
			                flag_grole=1
			                break
				    else:
					k=k+1

			    if flag_grole==0:
			          temp["g_role"]=0

			    word.append(temp)


		    elif start2 !=-1:
			right=j
			name=""
			for k in range(left,right+1):
			    name=name+text1[k]+" "
			name=name.strip(" ")
			temp["name"]=name
			temp["begin"]=left
			temp["end"]=right
			temp["s_number"]=s_number
			temp["id"]=j0
			j0=j0+1
			temp["ID"]=ID
			temp["gender"]=0
			if tag[right][1]=="NN" or tag[right][1]=="NNP":
			        temp["number"]=1
			elif tag[right][1] =="NNS" or tag[right][1]=="NNPS":
			        temp["number"]=-1
			else:
			        temp["number"]=0

			temp["person"]=0
			############################################################
			flag_lform=0
			for k in range(left,right+1):
			    if tag[k][1]=="NNP" or tag[k][1]=="NNPS":
			        temp["l_form"]=1
			        flag_lform=1
			        break
			if flag_lform==0:
			    for k in range(left,right+1):
			        if text1[k] in time and (right-left+1)<=3:
			            temp["l_form"]=4
			            flag_lform=1
			            break
			if flag_lform==0:
			    for k in range(left,right+1):
			        if tag[k][1]!="CD":
			            flag_lform=2
			            break
			    if flag_lform==0:
			        temp["l_form"]=4
			        flag_lform=1

			if flag_lform==2:
			    temp["l_form"]=2
			############################################################

			flag_grole=0
			k=right
			while k<len(tag) and k>=0 and k-right<=3:
			    if tag[k][1] in verb:
			        temp["g_role"]=1
			        flag_grole=1
			        break
			    else:
				k=k+1
			if flag_grole==0:
			    k=left
			    while k<len(tag) and k>=0 and left-k<=3:
				if tag[k][1] in verb:
				    temp["g_role"]=2
				    flag_grole=1
				    break
				else:
				    k=k-1
			if flag_grole==0:
			    k=right
			    while k<len(tag) and k>=0 and k-right<=3:
				if tag[k][1]=="IN":
				    temp["g_role"]=3
				    flag_grole=1
				    break
				else:
				    k=k+1
			if flag_grole==0:
			    temp["g_role"]=0

			word.append(temp)


	REF=[]
	for item in word:
	    if "X" not in item["ID"]:
		start=item["id"]
		flag_ref=0
		temp={}
		temp["ID"]=item["ID"]
                #if item["name"]=="National Broadcasting Co.":
                 #   print item
		if item["l_form"]!=3:  # item is not a pronoun 
		    word_anaphor=nltk.word_tokenize(item["name"])
                    #if item["name"]=="National Broadcasting Co.":
                     #   print word_anaphor

		    for j in range(start-1,-1,-1):
		        word_ante=nltk.word_tokenize(word[j]["name"])
		        if item["name"]==word[j]["name"] or item["name"] in word[j]["name"] or word[j]["name"] in item["name"]:
		            temp["ref"]=word[j]["ID"]
		            flag_ref=1
		            break
		        if word[j]["l_form"]!=3:
		            k2=len(word_anaphor)-1
		            while k2>=0:
		                k1=word_anaphor[k2]
		                k2=k2-1
		                if (k1 not in det) and (k1 not in prepo) and (k1 in word_ante):
		                    temp["ref"]=word[j]["ID"]
		                    flag_ref=1
		                    break
		            if flag_ref==1:
		                break
		        if word[j]["l_form"]!=3:   # identify acronym
		            temp2=""
		            for k1 in word_anaphor:
                                if k1[0].isupper() or k1[0].islower(): 
		                    temp2=temp2+k1[0]
                            
		            temp3=word[j]["name"]
                           # if item["name"]=="National Broadcasting Co.":
                            #    print temp2
                             #   print temp3
		            if temp2.lower()==temp3.lower():
		                temp["ref"]=word[j]["ID"]
		                flag_ref=1
		                break



		if flag_ref==0: 
		    antecedent=[]
		    for j in range(start-1,-1,-1):
		        if item["gender"]*word[j]["gender"]!=0 and item["gender"]*word[j]["gender"]!=1 and item["gender"]*word[j]["gender"]!=4:
		            continue
		        if item["number"]*word[j]["number"]==-1:
		            continue
		        if item["person"]*word[j]["person"]!=0 and item["person"]!=word[j]["person"]:
		            continue
		        if (item["l_form"]==4 and word[j]["l_form"]!=4) or (item["l_form"]!=4 and word[j]["l_form"]==4):
		            continue
		        if item["l_form"]==4 and word[j]["l_form"]==4:
		            word_anaphor=nltk.word_tokenize(item["name"])
		            word_ante=nltk.word_tokenize(word[j]["name"])
		            if "year" in word_anaphor and "number" in word_ante:
		                continue
		            if "number" in word_anaphor and "word" in word_ante:
		                continue
		        if item["l_form"]==3 and abs(item["s_number"]-word[j]["s_number"])>5: # item is a pronoun
		            break
		        antecedent.append(word[j])
		     
		    X=[]
		    for ante in antecedent:
		         X.append(derive_vector(ante,item))

                    if len(X)>0:
		        Y=clf.predict_proba(X)

		        prob=[]
		        for j in range(0,len(antecedent)):
		            temp1={}
		            temp1["index"]=j
		            temp1["h_distance"]=abs(antecedent[j]["id"]-item["id"])
		            temp1["prob"]=Y[j][1]
		            if antecedent[j]["l_form"]!=3:
		                word_anaphor=nltk.word_tokenize(item["name"])
		                word_ante=nltk.word_tokenize(antecedent[j]["name"])
		                for k in word_anaphor:
		                    if k in word_ante:
		                        temp1["prob"]=temp1["prob"]*2
		                        break

		            prob.append(temp1)

		        prob.sort(compare1)
		        if len(prob)!=0:
		            temp["ref"]=antecedent[prob[0]["index"]]["ID"]
		            flag_ref=1

		if flag_ref==0:
		    temp["ref"]=word[start-1]["ID"]


		REF.append(temp)

	#for item in REF:
	#   print item



	temp_file=preprocessed_file


	for item in REF:
	    ID=item["ID"]
	    ref=item["ref"]
	    str1="<COREF ID=\""+ID+"\">"
	    str2="<COREF ID=\""+ID+"\" REF=\""+ref+"\">"
	    temp_file=temp_file.replace(str1,str2)


	f = open(output_file_list[h1], "w") 
	f.write(temp_file)
	f.close

#################################################### end predict  ###############################################################
#################################################################################################################################




 


















