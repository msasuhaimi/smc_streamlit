# -*- coding: utf-8 -*-

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import re


df = pd.read_csv('SMCdf.csv')

st.title('Top 5 most popular tweets')

# Top 10 Most popular tweets (Likes, RT count)
#account_rep = 'Razer''HyperX''Logitech'
def topTen(account_rep):
	#Filters to specify Account, exclude replies and retweets
	filter1 = df['Account']== account_rep
	filter2 = df['In_reply']== 'none'
	filter3 = df['Is_RT']=='N'

	#groupby tweet_text and total or likes, rts, and engagement
	dftopten = df[filter1 & filter2 & filter3].groupby(['Tweet_Text'])['Favorite_count','Retweet_count', 'Engagement_count'].sum().fillna(0).sort_values(by = ['Engagement_count'],ascending = False).reset_index()

	#print
	st.header('Top 5 Most popular tweets for '+account_rep)
	for x in range(0,5):
			
		st.write('Status',x+1,': ',dftopten['Tweet_Text'][x])
		st.write('Likes: ',dftopten['Favorite_count'][x], 'Retweets: ', dftopten['Retweet_count'][x], 'Total Engagements',dftopten['Engagement_count'][x])

topTen('Razer')
topTen('HyperX')
topTen('Logitech')

st.title("Top 10 mentioned accounts")

def mentionAcc(account_rep):
	filter1 = df['Account']==account_rep
	filter2 = df['Mention']!='none'
	dffilter = df[filter1 & filter2]
	mention = dffilter['Mention'].value_counts().head(10)
	source = pd.DataFrame({
	  'Count' : mention
	}).reset_index()

	bars = alt.Chart(source).mark_bar().encode(
	  x='Count:Q',
	  y="index:O"
	)

	text = bars.mark_text(
	  align='left',
	  baseline='middle',
	  dx=3  # Nudges text to right so it doesn't appear on top of the bar
	).encode(
	  text='Count:Q'
	)
	
	st.header(account_rep)
	st.altair_chart((bars + text).properties(height=300))

mentionAcc('Razer')
mentionAcc('HyperX')
mentionAcc('Logitech')

st.title("Top 10 Hashtags used by Brand")

def topHashtag(account_rep):
	filter1 = df['Account']==account_rep
	filter2 = df['Hashtag']!='none'
	dffilter = df[filter1 & filter2]
	hashtag = dffilter['Hashtag'].value_counts().head(10)
	source = pd.DataFrame({
	  'Count' : hashtag
	}).reset_index()

	bars = alt.Chart(source).mark_bar().encode(
	  x='Count:Q',
	  y="index:O"
	)

	text = bars.mark_text(
	  align='left',
	  baseline='middle',
	  dx=3  # Nudges text to right so it doesn't appear on top of the bar
	).encode(
	  text='Count:Q'
	)
	
	st.header(account_rep)
	st.altair_chart((bars + text).properties(height=300))

topHashtag('Razer')
topHashtag('HyperX')
topHashtag('Logitech')

st.title("Number of Tweets per week")

def tweetPDay(account_rep):
	# Create subset with filters
	dfyear = df[df['Year']==2021]
	#could not use Year as filter, takes too long; might crash

	filter1 = dfyear['Account']==account_rep
	filter2 = dfyear['Is_RT']=='N'
	#filter3 = dfyear['Month']=='Dec'
	dfyearF = dfyear[filter1 & filter2]

	dfgb = dfyearF.groupby(['month_week'],sort=False)['Full_Date'].count().reset_index()
	dfgb.rename(columns={'Full_Date':'Tweet_count'},inplace=True)
	#Create line chart
	week = alt.Chart(dfgb[::-1]).mark_line(point=alt.OverlayMarkDef(color="red")).encode(
	  alt.X('month_week',sort=None, axis=alt.Axis(title='Month, Week')),
	  y='Tweet_count',
	  tooltip=['Tweet_count']
	)
	st.header(account_rep)
	st.altair_chart(week)

tweetPDay('Razer')
tweetPDay('HyperX')
tweetPDay('Logitech')

st.title("Number of Tweet Engagement per week")

def engagePDay(account_rep):
	# Create subset with filters
	dfyear = df[df['Year']==2021]

	#could not use Year as filter, takes too long; might crash
	filter1 = dfyear['Account']==account_rep
	filter2 = dfyear['Is_RT']=='N'
	#filter3 = dfyear['Month']=='Dec'
	dfyearf = dfyear[filter1 & filter2]

	#list of date and number of tweets per date
	frequencyD = dfyearf.groupby(['month_week'],sort=False, as_index=False)['Full_Date','Retweet_count','Favorite_count','Engagement_count'].sum()

	#Create line chart
	week = alt.Chart(frequencyD[::-1]).mark_line(point=alt.OverlayMarkDef(color="red")).encode(
	  alt.X('month_week',sort=None, axis=alt.Axis(title='Date')),
	  y='Engagement_count',
	  tooltip=['Retweet_count','Favorite_count','Engagement_count']
	  )
	  
	st.header(account_rep)
	st.altair_chart(week)

engagePDay('Razer')
engagePDay('HyperX')
engagePDay('Logitech')
