from urlextract import URLExtract
import emoji as ji
from collections import Counter
import pandas as pd
ue = URLExtract()
from wordcloud import WordCloud
wc = WordCloud(height=600, width=600, min_font_size=10, background_color='white')
import matplotlib.pyplot as plt
import datetime as dt



def featch_data(user, df):

    if user == "Group_analysis":
     #Number of words  
     words = []
     for i in df['Message']:
        words.extend(i.split())
     #Number of shared media
     q = df[df['Message'] == '<Media omitted>'].values 

     #Number of URL's

     URL = []
     for i in df['Message']:
        URL.extend(ue.find_urls(i))   
    
     return df.shape[0], len(words), len(q), len(URL)

    else:
        nd = df[df['Name'] == user]
        words = []
        for i in nd['Message']:
           words.extend(i.split())

        #Number of shared media
        w = nd[nd['Message'] == '<Media omitted>'].values    

        #Number of URl
        URL = []
        for i in nd['Message']:
         URL.extend(ue.find_urls(i))  

        return df[df["Name"] == user].shape[0], len(words), len(w), len(URL)
    

def MAU(df):
    x = df['Name'].value_counts()
    #To find the percentage 
    per = round(df['Name'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'count':'Percentage'})
    return x, per

def woc(df, selec_user):
   if selec_user != 'Group_analysis':
      df = df[df['Name'] == selec_user]   
   df = df[df['Message'] != '<Media omitted>']
   s = wc.generate(df['Message'].str.cat(sep=" "))

   return s

def top_25(df, selec_user):
   if selec_user != 'Group_analysis':
      df = df[df['Name'] == selec_user]
   
   df = df[df['Message'] != '<Media omitted>']
   s = wc.generate(df['Message'].str.cat(sep=" "))
   top_words = list(s.words_.keys())
   top_25 = []
   for i in range(25):
    top_25.append(top_words[i])   
  
   wo = []
   for i in df['Message']:
     wo.append(i) 

   wo = ' '.join(wo)

   wo = wo.split()

   feq = []
   for i in top_25:
      w = 0
      for j in wo:
         if i == j:
            w += 1
      feq.append(w)     

   return top_25, feq


def emoji(df, selec_user):
    if selec_user != 'Group_analysis':
      df = df[df['Name'] == selec_user]

    emo = []
    for i in df['Message']:
        emo.extend([c for c in i if c in ji.EMOJI_DATA])

    emo_counter = Counter(emo)

    result = pd.DataFrame(emo_counter.most_common(), columns= ['Emoji', 'Count'] )

    return result

def tl(df, selec_user):
   if selec_user != 'Group_analysis':
      df = df[df['Name'] == selec_user]
   timeline = df.groupby(['Year', 'Month'])['Message'].count().reset_index()
   t = []
   for i in range(timeline.shape[0]):
      t.append(timeline['Month'][i] + "-" + timeline['Year'][i])
   timeline['time'] = t
   ndf = timeline.drop(columns=['Year', 'Month'])

   return ndf

def dtl(df, selec_user):
   if selec_user != 'Group_analysis':
      df = df[df['Name'] == selec_user]
   timeline = df.groupby(['Year', 'Month', 'Day'])['Message'].count().reset_index()
   t = []
   for i in range(timeline.shape[0]):
      t.append(timeline['Day'][i] + '-' + timeline['Month'][i] + '-' + timeline['Year'][i])
   timeline['time'] = t
   dmy = timeline.drop(columns= ['Day', 'Month', 'Year']) 

   return dmy     

def MAD(df):

   ymd = df.groupby(['Year','Month','Day'])['Message'].count().reset_index()
   for i in range(ymd['Year'].shape[0]):
      ymd['Year'][i] = str(20) + ymd['Year'][i]

   for i in range(ymd['Day'].shape[0]):
      if ymd['Day'][i][:-1] == '':
         ymd['Day'][i] =  str(0) + ymd['Day'][i]

   for i in range(ymd['Month'].shape[0]):
      if ymd['Month'][i][:-1] == '':
         ymd['Month'][i] =  str(0) +  ymd['Month'][i]  
   
   ymd.loc[14, 'Day'] = '01'

   ymd["Day"] = ymd["Day"].astype(str)

   ddf = []
   for i in range(ymd.shape[0]):
      ddf.append(ymd['Year'][i] +'-'+ ymd['Month'][i] +'-'+ ymd['Day'][i])      

   ymd['Date'] = ddf

   ymd['Date'] = pd.to_datetime(ymd['Date'])
   ymd['dname'] = ymd['Date'].dt.day_name()      

   fa = ymd['dname'].value_counts().reset_index()

   return fa

def HeatMap(df):

   hm = df.groupby(['Year','Month','Day','Hour'])['Message'].count().reset_index()

   for i in range(hm['Year'].shape[0]):
     hm['Year'][i] = str(20) + hm['Year'][i]

   for i in range(hm['Day'].shape[0]):
     if hm['Day'][i][:-1] == '':
        hm['Day'][i] =  str(0) + hm['Day'][i]

   for i in range(hm['Month'].shape[0]):
      if hm['Month'][i][:-1] == '':
         hm['Month'][i] =  str(0) +  hm['Month'][i]   

   hm.loc[22, 'Day'] = '01'

   thm = []
   for i in range(hm.shape[0]):
      thm.append(hm['Year'][i] +'-'+ hm['Month'][i] +'-'+ hm['Day'][i])    

   thm = pd.DataFrame(thm, columns=['Date'])

   hm['Date'] = thm

   import datetime as dt

   hm['Date'] = pd.to_datetime(hm['Date'])
   hm['dname'] = hm['Date'].dt.day_name()
   return hm         
