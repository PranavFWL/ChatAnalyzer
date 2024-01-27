import streamlit as st
import pandas as pd
import re 
import matplotlib.pyplot as plt
import WMAhelper 
from collections import Counter
from wordcloud import WordCloud as wc
import seaborn as sns


def con(data):
  #a = open(t, 'r', encoding='utf-8')
  #data = a.read()

  paaa =r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s[APMapm]{2}) - ([A-Za-z\s]+):\s(.+)"
  n_data = re.findall(paaa, data)
  
  string_list = [str(item) for item in n_data]

    # Using join to convert the list to a string with a space as the delimiter
  new_data = ' '.join(string_list)

  def convert(w):
    con = 0
    if w[10:] == 'PM':    #single
        q = int(w[:-11]) + 12 
        con = str(q) +':'+ w[2:-8]

    if w[11:] == 'PM':
        q = int(w[:-11]) + 12
        con = str(q) + w[2:-8]

    if w[-2:] == 'AM':
        con = (w[:-8])      


    return con  
  

  e_data = new_data.replace('"',"'")

  patt = r"(\d{1,2}:\d{2}\\u202f[APMapm]{2})"
  time = re.findall(patt, new_data)

  pat = r", '([A-Z][a-z]+(?: [A-Z][a-z]+)?)',"
  name = re.findall(pat, new_data)

  h24 = []
  for i in time:
    h24.append(convert(i))

  pat = r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s[APMapm]{2}\s-\s.*)"
  message = re.findall(pat, e_data) 

  mess = re.findall(r"'([^']+)'[)]", e_data)

  pattern = r"(\d{1,2}/\d{1,2}/\d{2,4})"
  date = re.findall(pattern, new_data)

  patt = r"/\d{1,2}/"
  day = re.findall(patt, new_data)[1:]
    
    # Using join to convert the list to a string with a space as the delimiter
  string_list = [str(item) for item in day]
  day = ' '.join(string_list)

  pa = r"\d{1,2}"
  day = re.findall(pa, day)

  patt = r"\d{1,2}/\d{1,2}"
    #month = re.findall(patt, new_data)
  pa = r"'\d{1,2}/"
  month = re.findall(pa, new_data)

    # Using join to convert the list to a string with a space as the delimiter
  string_list = [str(item) for item in month]
  month = ' '.join(string_list)

  pa = r"\d{1,2}"
  month = re.findall(pa, month)

  patt = r"/\d{1,2},"
  year = re.findall(patt, new_data)
    
    # Using join to convert the list to a string with a space as the delimiter
  string_list = [str(item) for item in year]
  year = ' '.join(string_list)

  pa = r"\d{1,2}"
  year = re.findall(pa, year)


    # Using join to convert the list to a string with a space as the delimiter
  string_list = [str(item) for item in h24]
  h24 = ' '.join(string_list)

  pa = r"\d{1,2}:"
  ho = re.findall(pa, h24)
  pt = r":\d{1,2}"
  min = re.findall(pt, h24)

  hour = []
  minutes = []
  for i in ho:
      hour.append(i[:-1])

  for j in min:
     minutes.append(j[1:])

  df = pd.DataFrame({'Year': year, 'Month':month, 'Day':day, 'Hour': hour, 'Minutes': minutes, 'Name': name, 'Message': mess})   
  
  return df

#DISPLAY


st.sidebar.title('Sentiment Analyser')

a = st.sidebar.file_uploader('Upload your text file', type= ['txt'])

#The file right now is in form of stream, we have to convert it into a string
if a is not None:
  file = a.getvalue()
  bata = file.decode('utf-8')

  df = con(bata)

#ANALYSIS OF DATA

#featech unique data

  user_list = df['Name'].unique().tolist()
  user_list.sort()
  user_list.insert(0,"Group_analysis")

  selec_user= st.sidebar.selectbox("Show analysis of ",user_list)
  
  
  if st.sidebar.button('Show analysis'):
     
     st.write('Analysis for ',selec_user)

     total_messages, words, om, url = WMAhelper.featch_data(selec_user, df)

     #1.Stats

     col1, col2, col3, col4 = st.columns(4)

     with col1:
        st.header("Total messsages ")
        st.title(total_messages)


     with col2:
        st.header(' Total words')
        st.title(words)

     #SHARED MEDIA COUNT

     with col3:
        st.header('Shared media')
        st.title(om)
     
     with col4:
        st.header('Shared URL')
        st.title(url)


      #Most active users in the group only for Group_analysis
        
     if selec_user == 'Group_analysis':
       st.title('Users Activity')
       x, per = WMAhelper.MAU(df)
       fig, b = plt.subplots()

       col1, col2 = st.columns(2)

       with col1:
          b.bar(x.index, x.values, color='red')
          plt.xticks(rotation= 'vertical')
          st.pyplot(fig)

       with col2:
          st.dataframe(per)   

     st.title('Word Cloud')
     plo = WMAhelper.woc(df, selec_user)
     fig, b = plt.subplots()
     b.imshow(plo)
     st.pyplot(fig)
     
     st.title('Top 25 words')
     top_25, feq = WMAhelper.top_25(df, selec_user)
     re_fd = pd.DataFrame(list(zip(top_25,feq)),columns=['Words', 'Frequency'])

     fig, bb = plt.subplots()
     bb.barh(re_fd['Words'], re_fd['Frequency'])
     plt.xticks(rotation = 'vertical')
     st.pyplot(fig)

     st.title('Emojis')
     emo  = WMAhelper.emoji(df, selec_user)

     col5, col6 = st.columns(2)

     with col5:
       st.dataframe(emo)

     with col6:
       fx, ac = plt.subplots()
       ac.bar(emo['Emoji'], emo['Count'])
       st.pyplot(fx)

     ndf = WMAhelper.tl(df, selec_user) 
     st.title('Activity in Month&Year')
     zig, c = plt.subplots()
     c.plot(ndf['time'], ndf['Message'])
     plt.xticks(rotation= 'vertical')
     st.pyplot(zig)

     dmy = WMAhelper.dtl(df, selec_user)
     st.title('Activity on each day')
     zac, d = plt.subplots()
     d.plot(dmy['time'], dmy['Message'])
     plt.xticks(rotation= 'vertical') 
     st.pyplot(zac)
      
     fa = WMAhelper.MAD(df)
     st.title('User Activity as per Day') 
     vix, e = plt.subplots()
     e.bar(fa['dname'], fa['count'])
     plt.xticks(rotation= 'vertical')
     st.pyplot(vix)
     
     st.title('HeatMap')
     HM = WMAhelper.HeatMap(df)
     plt.yticks(rotation= 'horizontal')
     lig, q = plt.subplots(figsize= (50,20))
     q.yaxis.tick_left()
     q.tick_params(axis='both', which='both', labelsize=50)
     sns.heatmap(HM.pivot_table(index='dname', columns='Hour', values='Message', aggfunc='count').fillna(0))
     st.pyplot(lig)
     



     



          

       
          

          
             
  


