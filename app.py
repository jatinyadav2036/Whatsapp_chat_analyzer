import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

from helper import most_common_words

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    #fetch unique users
    user_list = df['User'].unique().tolist()
    # user_list.remove('None')
    user_list = [user for user in user_list if user is not None]
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages ,words,num_media,links = helper.fetch_stats(selected_user,df)
        #Stat Area
        st.title("Top Statistics")
        col1 ,col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(links)

        #monthly timeline
        timeline = helper.month_analysis(selected_user,df)
        st.title("Monthly Timeline")
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        daily_timeline = helper.daily_analysis(selected_user,df)
        st.title("Daily Timeline")
        fig,ax = plt.subplots(figsize = (18,10))
        ax.plot(daily_timeline['date'], daily_timeline['message'],color = '#9C27B0',linewidth = 2)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #week activity map
        st.title("Activity Map")

        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_acivity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            month_day = helper.month_acivity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_day.index, month_day.values,color ='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        if user_heatmap.empty:
            st.warning("No activity data available for this user.")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            ax.set_ylabel("Day of the Week", fontsize=12)
            ax.set_xlabel("Hour of the Day", fontsize=12)
            st.pyplot(fig)

        #finding  most user in group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x ,new_df= helper.most_busy_user(df)
            fig , ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        common = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(common[0],common[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        # st.dataframe(most_common_words, use_container_width=True, hide_index=True)

        #emoji analysis
        plt.rcParams['font.family'] = 'Segoe UI Emoji'
        emoji_df = helper.emoji_analysis(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df["count"].head(), labels=emoji_df["emoji"].head(), autopct="%0.2f")
            st.pyplot(fig)


