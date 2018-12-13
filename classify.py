import pickle
import numpy as np
import re

def stop_words():
    s = "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves"
    l = s.split()
    l1 = [w.replace("'","") for w in l] #remove apostrophes
    return l1

def removeStopWords(line):
    wordsList = line.split()
    wordsList = [re.sub(r'\W+', '', word) for word in wordsList] #remove alphanumeric character
    filtered = filter(lambda word: re.match(r'\w+', word), wordsList) #atleast of length 1
    words_lower = [word.lower() for word in filtered] #convert to lower case
    clean_words_any = [re.sub("[^a-z]", "",word) for word in words_lower] #remove special characters
    clean_words = filter(lambda word: re.match(r'\w+', word), clean_words_any) #atleast of length 1 after removing the special characters
    stop_words_list = stop_words() #get the stop words
    filtered_words = list(filter(lambda word: word not in stop_words_list, clean_words)) #check for stop words
    return filtered_words

def get_job_title(description):
	word_list = removeStopWords(description)

	with open("data/vocabdict.pkl",'rb') as fp: # load the vocabulary dictionary
		vocab_dict = pickle.load(fp)

	coeff_mat = np.load('data/coeff_array.npy') #load the coefficient matrix containig weights 
	intercepts = np.load('data/inter_array.npy')

	labels = {16: 'network admin engineer', 14: ' EE embedded engineer / firmware engineer', 8: 'security engineer', 2: 'test engineer/qa engineer', 5: 'data scientist/big data engineer/machine learning engineer', 7: 'medical engineer', 13: 'architect', 6: 'sales representative/marketing representative/customer representative', 9: 'support helpdesk', 15: 'administrative coordinator/hr', 11: 'technician', 17: 'ui-ux designer', 20: 'mechanical engineer', 3: 'product manager', 10: 'web developer/mobile developer', 4: 'system admin engineer', 0: 'software engineer', 12: 'researcher academia', 18: 'database developer/database admin', 1: ' business analyst/data analyst', 19: 'consultant'}

	dvec = np.zeros(len(vocab_dict), np.int)

	for word in word_list:
		if word in vocab_dict:
			dvec[vocab_dict[word]] = 1

	ans_array = coeff_mat.dot(dvec)
	ans = labels[ans_array.argmax(axis=0)]
	return ans

if __name__ == "__main__":
	jd1 = "I am a passionate coder. I like coding in java, python and I am good with developing big data and machine learning pipelines. I like working in an agile environment where i get to implment meaningful service and work together with a good team."
	jd2 = "managing teams and developing software products to solve the customer problems by using agile methodology"
	print(get_job_title(jd1))
	print(get_job_title(jd2))
