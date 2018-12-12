# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
import re
# Create your views here.

def index1(request): #定义视图index1 
    print(request.GET["id"])
    print(settings.DATABASES)
    print(settings.MONGO_URL)
    jid=request.GET["id"]
    result = query_mongo_by_jid(jid)
    result["htmlized_jd"] = process_jd(result)
    result["jid"] = result["_id"]
    #ans={} #创建一个字典
    #ans['head']='hello world' # 赋值
    return render(request,'app001/jobpage.html',result)

def query_mongo_by_jid(jid):
    result = settings.MONGO_COLLECTION.find_one({"_id":jid})
    return result

def process_jd(mongo_doc):
    jd=mongo_doc["job_description"]
    html_jd = htmlize(jd)
    tagged_jd = highlight_jd_words(mongo_doc["tfidf_imp_words"], html_jd, '<span class="highlight">', '</span>')
    return tagged_jd


def htmlize(jd):
    paragraphs = jd.split('\n')
    new_jd = ' </p> <p> '.join(paragraphs)
    new_jd = ' <p> ' + new_jd + ' </p> '
    return new_jd


# lowercase, remove punctuation, numbers
def filter_word_for_match(word):
    if(re.match("\<.*", word) or re.match(".*\>", word)):  #html tag
        fword = word
    else:
        fword=re.sub("[^a-z]", "",word.lower())
    return fword

# enclose word from highlight_wordset
def highlight_jd_words(highlight_wordset, html_jd, tag_bgn, tag_end):
    html_jd_words = html_jd.split()
    in_highlight=False
    new_jd_words = []
    for w in html_jd_words:
        filter_w = filter_word_for_match(w)
        if(filter_w in highlight_wordset):
            if(in_highlight):
                new_word=w
            else:
                new_word=tag_bgn+" "+w
                in_highlight=True
        else:
            if(in_highlight):
                new_word = tag_end + " " + w
                in_highlight=False
            else:
                new_word = w
        new_jd_words.append(new_word)
    if(in_highlight):
        new_jd_words.append(tag_end)
    new_jd=' '.join(new_jd_words)
    return new_jd

## add <span class="highlight"> to surround focused words (method="word"), or sentences (method="sentence")
#def apply_cluster_to_jd(reversed_model, highlight_cids, html_jd, method, tag_bgn, tag_end):
#    html_jd_words = html_jd.split()
#    new_jd_words = []
#    if(method == "word"):
#        in_highlight = False
#        for w in html_jd_words:
#            filter_w = filter_word_for_match(w)
#            if(filter_w in reversed_model and reversed_model[filter_w] in highlight_cids):
#                if(in_highlight):
#                    new_word=w
#                else:
#                    new_word=tag_bgn+" "+ w
#                    in_highlight=True
#            else:
#                if(in_highlight):  #last word is in highlight
#                    new_word = tag_end + " " +w
#                    in_highlight=False
#                else:
#                    new_word = w
#            new_jd_words.append(new_word)
#        if(in_highlight):  # if still in highlight in the end, close the tag
#            new_jd_words.append(tag_end)
#    new_jd = ' '.join(new_jd_words)
#    return new_jd
