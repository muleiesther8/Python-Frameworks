import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

# Load and prepare data
df = pd.read_csv("metadata.csv", low_memory=False)
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# App title and intro
st.title("📚 CORD-19 Data Explorer")
st.write("An interactive dashboard exploring COVID-19 research papers from the CORD-19 dataset.")

# Filter by year range
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.slider("Select year range", min_year, max_year, (2020, 2021))

# Filtered data
df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show sample data
st.subheader("📄 Sample Data")
st.dataframe(df_filtered[['title', 'authors', 'journal', 'year']].head(10))

# Publications over time
st.subheader("📊 Publications by Year")
year_counts = df_filtered['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values, color='skyblue')
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
st.pyplot(fig1)

# Top journals
st.subheader("🏢 Top 10 Journals")
top_journals = df_filtered['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_journals.plot(kind='bar', color='lightcoral', ax=ax2)
ax2.set_xlabel("Journal")
ax2.set_ylabel("Number of Papers")
st.pyplot(fig2)

# Word Cloud
st.subheader("☁️ Word Cloud of Paper Titles")
stop_words = set(stopwords.words('english'))
titles_text = " ".join(str(title) for title in df_filtered['title'].dropna())
wordcloud = WordCloud(width=1000, height=600, background_color='white', stopwords=stop_words).generate(titles_text)
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)

st.write("✅ **Dashboard complete!** You can explore by changing the year range above.")
