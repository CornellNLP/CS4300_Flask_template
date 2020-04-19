#!/usr/bin/env python
# coding: utf-8

# In[108]:


import csv


# In[109]:


twitter_info_list = []
with open('twitter_info.csv') as file:
    reader = csv.reader(file, delimiter=",")
    line_count = 0
    for line in reader:
        if line_count == 0:
            print("starting...")
            line_count += 1
        else:
            element = {"State": line[0], "Name": line[1], "Handle": line[2][1:]}
            twitter_info_list.append(element)
    print("done")


# In[110]:


#change to dictionary format for all tweets, with each column titled (maybe not ones we don't need)
all_states = {}
Maryland = []

with open("data/Maryland.csv") as file:
    reader = csv.reader(file, delimiter=",")
    line_count = 0
    for line in reader:
        d = {}
        if line_count == 0:
            columns = line
            print(columns)
            line_count += 1
        else:
            d["id"] = line[0]
            d["date"] = line[3]
            d["time"] = line[4]
            d["username"] = line[7]
            d["tweet"] = line[10].lower()
            d["mentions"] = line[11]
            d["urls"] = line[12]
            d["photos"] = line[13]
            d["hashtags"] = line[17]
            d["link"] = line[19]
            line_count += 1
            Maryland.append(d)

    print(line_count)


# In[111]:


print(len(Maryland))
print(Maryland[1])


# In[112]:


#all direct mentions of the disease
direct_mentions = []
tf_mention = []
for elem in Maryland:
    if "covid19" in elem["hashtags"] or "coronavirus" in elem["hashtags"] or "coronavirus" in elem["tweet"] or "covid" in elem["tweet"]:
        direct_mentions.append(elem)
        tf_mention.append((elem["date"], True))
    else:
        tf_mention.append((elem["date"], False))


# In[113]:


print(Maryland[1])


# In[114]:


#first mention
first_mention = direct_mentions[len(direct_mentions)-1]
first_mention_date = first_mention["date"]
print(first_mention_date)


# In[115]:


#proportion of mentions of disease vs. other
proportion_mentions = len(direct_mentions)/len(Maryland)
print(proportion_mentions)


# In[116]:


#rolling average
def rolling_avg(lst):
    last_seven = 0
    lst.reverse()
    for date, tf in lst:
      #  print(tf)
        if tf == True and last_seven < 7:
            last_seven += 1
        elif tf == False and last_seven > 0:
            last_seven -= 1
      #  print(last_seven)
        curr_avg = last_seven/7
        print(curr_avg)


# In[117]:


rolling_avg_list = rolling_avg(tf_mention)


# In[107]:


print(first_mention_date)
print(proportion_mentions)


# In[ ]:
