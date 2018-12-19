# This program import the json file with data collected from the Depression Forum on DailyStrength.org and
# store them into a text file. The json file is first prodessed to ensure proper format and data were extracted
# before and after saved to the text files. The texts in the comments of the saved file is further processed and
# performed sentiment analysis. The result is again saved to another text file.

import json
from pprint import pprint
import os
import nltk.data
from pycorenlp import StanfordCoreNLP
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Connect to standford-corenlp server in command line:
# cd stanford-corenlp-full-2016-10-31
# java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

DATA_ROOT = '/Users/mengtsai/Desktop/Ind_study/tutorial'
data_path = os.path.join(DATA_ROOT, 'depress_post.json')
print(data_path)

# write comments data to a separate txt file
f1 = open('depress_p1_test.txt', "w")

with open(data_path) as json_data:
    data = json.load(json_data)

# Clean whitespace and comma in post/comment, then save to a text file for sentiment analysis later.
    k= 0
    for r in data:
        k=k+1
        pp = r['comment']
        if len(pp)==0:
            pp= r['comments']

        # stripped the whitespace from the beginning and the end of the string
        if len(pp)<>0:
            ps=pp[0].replace(u'\xa0', u' ').strip()
            num_words = len(ps.lower().split())
            if num_words < 25:
                ps = ps.replace(',', ' ')
            ps=ps.replace(',','. ')

            for i in range(0, len(pp) - 1):
                ps = ps + " "+ pp[i + 1].replace(u'\xa0', u' ').strip()

                # Find the long string without a period
                num_words = len(ps.lower().split())
                if num_words > 30:
                    ps = ps.replace(',', '. ')
                    period = ps.count('.')
                    if period == 0:
                        print k
                ps = ps.replace(',', ' ')

            # Find and replace repeated punctuation?
            ps = ps.replace(',', '. ')
            ps = ps.replace('...', '.')
            ps = ps.replace(';','.')
            ps = ps.replace('!!!','!')
            ps = ps.replace('-',' ')
            ps = ps.replace('\"','\'')

            f1.write(ps + "\n")
            #print (ps)

    f1.close()


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
f1 = open('depress_p1_test.txt', "r")
# (option: write to a .csv file)
f2 = open('depress_p1_sentiment.txt', "wb")

# For comment
#f2.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % ("author","a_id","time","int_time","date","title","replyTo","mood","comment",
#          "reply_ct","num_chars","num_words","num_uwords","total","v_pos","positive","neutral","negative","v_neg"))

# For post
f2.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" %("author","a_id","time","int_time","date","title","mood","post","reply_ct",
                    "num_chars","num_words","num_uwords","total","v_pos","positive","neutral","negative","v_neg"))

with open(data_path) as json_data:
    data = json.load(json_data)

    for r in data:
        pp = r['comment']
        if len(pp)==0:
            pp= r['comments']

        # Check if the comment is empty, if not assign time interval, author...of each comment in the file

        if len(pp)<>0:
            time = r['time'][11:19]
            date = r['date']
            title = r['title'][0].replace(u'\xa0', u' ').strip()
            title = title.replace(',', ' ')
            reply_ct = r['reply_ct']
            mood = r['mood'][20:]
            mood = mood.replace('-sm __mood-icon\"></i>', '')

            # Assign time interval
            if time < '06:00:01':
                int_time = 'midnight'
            elif (time > '06:00:00') & (time < '12:00:01'):
                int_time = 'morning'
            elif (time > '12:00:00') & (time < '18:00:01'):
                int_time = 'afternoon'
            else:
                int_time = 'night'

            # For comment :
            # a_id= r['a_id'][15:]
            # replyTo = r['reply-to'][0].replace(u'\xa0', u' ').strip()
            # author = r['author']

            # For post only:
            author = r['author'][0]
            a_id = r['a_id'][0][15:]
            ps=pp[0].replace(u'\xa0', u' ').strip()
            num_words = len(ps.lower().split())
            if num_words > 32:
                ps = ps.replace(',', '. ')
            ps=ps.replace(',',' ')

            # stripped the whitespace at the beginning and end of the string
            for i in range(0, len(pp) - 1):
                ps = ps + pp[i + 1].replace(u'\xa0', u' ').strip()
                num_words = len(ps.lower().split())
                if num_words < 25:
                    ps = ps.replace(',', ' ')
                ps = ps.replace(',', '. ')

            # Find the total number of char, words, unique words in each post/comment
            num_chars = len(ps)
            num_words = len(ps.lower().split())
            num_uwords = len(set(ps.lower().split()))

            ps = ps.replace(',', '. ')
            ps = ps.replace('...', '.')
            ps = ps.replace(';', '.')
            ps = ps.replace('-',' ')
            ps = ps.replace('"', '\'')

            # write to the comment file
            #f2.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, " %(author,a_id,time,int_time,date,title,replyTo,mood,ps,reply_ct,num_chars, num_words, num_uwords))

            # write to the post file
            f2.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d, " %(author,a_id,time,int_time,date,title,mood,ps,reply_ct,num_chars, num_words, num_uwords))

            for line in f1:
                dt = tokenizer.tokenize(line)
                print(len(dt), dt)

                # Sentiment analysis begins here
                total = 0
                vpos = 0; pos = 0; neu = 0; neg = 0; vneg = 0
                nlp = StanfordCoreNLP('http://localhost:9000')
                for j in range(0, len(dt)):

                    res = nlp.annotate(dt[j],
                                   properties={
                                       'annotators': 'sentiment',
                                       'outputFormat': 'json',
                                       'timeout': 10000,
                                   })
                # Calculate sentiment score and print out

                    for s in res["sentences"]:
                        print "%s: %s %s" % (
                            #   s["index"],
                            " ".join([t["word"] for t in s["tokens"]]),
                            s["sentimentValue"], s["sentiment"])
                        if s["sentiment"] == "Verypositive":
                            score = 5
                            vpos += 1
                        elif s["sentiment"] == "Positive":
                            score = 4
                            pos += 1
                        elif s["sentiment"] == "Neutral":
                            score = 3
                            neu += 1
                        elif s["sentiment"] == "Negative":
                            score = 2
                            neg += 1
                        elif s["sentiment"] == "Verynegative":
                            score = 1
                            vneg += 1

                    print('score= ', score)

                    total += score

                # Save posts/comments sentiment results to a file
                
                f2.write("%d, %d, %d, %d, %d, %d\n" % (total, vpos, pos, neu, neg, vneg))
                break

        print("Total= " + str(total))
        print("Very positive: %d, Positive: %d, Neutral: %d" % (vpos, pos,neu))
        print("Very negative: %d, Negative: %d\n" % (vneg, neg))

f2.close()
f1.close()



