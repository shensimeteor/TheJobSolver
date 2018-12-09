1. step1_download_mongo_jobtitles.py:  download all jobs titles (in jobs_infos.csv) from MongoDB.appDatabase.jobs

2. step2_get_basic_cleaned_jobtitles.py:  clean job title (preliminarily).  Output: jobs_infos_cleaned3.csv. Also output words_list.txt, i.e. the words appeared in the cleaned job titles.

   step2.1_cleaned_jobtitles_stats.py: show distribution of how long (number of words) of each job title
   step2.2_filter_jts_by_nwords.py: filter jobs by limit the length (number of words) in job title (here, by 5)
       output: jobs_infos_cleaned3_filter5.csv

3. step3_word2vec.py: download wordvector from MongoDB.appDatabase.vecdata_wiki_news, for word in words_list.txt. output: wordvectors.pkl 

4. step4_average_vec.py: calculate each job title's vector, by averaging words' vector of each job title
      input: jobs_infos_cleaned3_filter5.csv,  wordvectors.pkl
      output: jt_vector.pkl
---
for hierachical clustering, need cosine similarity matrix (huge), so only some jobs are used (5% randomly sampled).
- step4.1_sample_jt_vectors.py: get the randomly sampled (5%) jobs titles vector: jt_vector_sampled.pkl
- step5_cluster_jts.py: do the hierachical clustering with jt_vector_sampled.pkl. Output to cluster_results/*

---
for kmeans clustering, SKlearn provides a efficient method (MinBatchKmeans) to cluster for all the data.
- step6_cluster_all_kmeans.py: use kmeans to cluster all job titles. Output to cluster_results/kmeans_cleaned3_filter5_average_full/new_200_clusters/:  cluster_???.txt (all job id/titles clustered to ??? cluster);  summary.csv/txt (each cluster id, size, and its high frequent worrds)
  (use k=200)
- Check cluster_results/kmeans_cleaned3_filter5_average_full/new_200_clusters/{summary.csv,cluster_???.txt} and manually label/merge some clusters. Then put it into new_200_clusters/labels_1st.txt, also copy everything from cluster_results/kmeans_cleaned3_filter5_average_full/new_200_clusters to cluster_results_save/new_200_clusters. 

- step7_apply_labels_and_rest_cluster.py:  Because the 1st k=200 clusters can't cluster well for several labels, I did another clustering, for the jobs that haven't be labeled yet. Here, k=500, for the unlabeled job titles.
  Ouput: cluster_results/kmeans_cleaned3_filter5_average_2nd/ 
- similary, label/merge clusters, and put it into labels_2nd.txt, then copy to cluster_results_save/2nd_500_clusters/

- step8_apply_2labels.py: to apply labels (from 2 clusters) to job titles, output: labeled_results/*, i.e. each label as a file, saving job ids & job titles (cleaned)

- step9_upload_labels_mongodb.py: upload labeled_results/* to MongoDB.appDatabase.jobs.job_title_label
