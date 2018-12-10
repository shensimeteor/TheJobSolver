This code is:
1. to get the vocabulary / words-with-freq from mongodb job_description_cleaned field, output to vocab_cleanedJD.csv (word,count)
  - done by: get_vocab_size.py 
  - size is very large, about 1million
2. to remove low-freq words in mongodb job_description_cleaned (count<100), and upload to mongodb as new field: job_description_cleaned2
  - about: 24K words
