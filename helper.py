from pandas import DataFrame
from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
extract = URLExtract()
from collections import Counter
import emoji


def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media = df[df["message"].str.contains("media omitted", case=False, na=False)].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return df.shape[0],len(words),num_media,len(links)

def most_busy_user(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'User': 'Name', 'count': 'Percent'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    temp = df[df['User'].notna()]
    temp = temp[~temp["message"].str.contains("media omitted", case=False, na=False)]
    temp = temp[~temp["message"].str.contains("message", case=False, na=False)]
    temp = temp[~temp["message"].str.contains("deleted", case=False, na=False)]

    def remove_stopwords(message):
        y =[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500,min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc



def most_common_words(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    temp = df[df['User'].notna()]
    temp = temp[~temp["message"].str.contains("media omitted", case=False, na=False)]
    temp = temp[~temp["message"].str.contains("message", case=False, na=False)]
    temp = temp[~temp["message"].str.contains("deleted", case=False, na=False)]


    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words = pd.DataFrame(Counter(words).most_common(20))
    #
    # most_common_words.insert(0,'Rank', range(1, len(most_common_words) + 1))
    # most_common_words.reset_index(drop=True, inplace=True)
    return most_common_words

def emoji_analysis(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])


    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=["emoji", "count"])

    return emoji_df


def month_analysis(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_analysis(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby(['date']).count()['message'].reset_index()
    return daily_timeline

def week_acivity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def month_acivity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    return df['month_name'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(
        0)

    return user_heatmap