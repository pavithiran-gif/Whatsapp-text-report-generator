import streamlit
import preprocessor
import helper

from matplotlib import pyplot
import seaborn

streamlit.set_page_config(page_title='Whatsapp Chat Analyser',
                          layout='wide', initial_sidebar_state='auto')
streamlit.sidebar.title('Whatsapp Chat Analysis')

uploadedFile = streamlit.sidebar.file_uploader('Choose a File')
if uploadedFile is not None:
    bytesData = uploadedFile.getvalue()
    data = bytesData.decode('utf-8')
    dataFrame = preprocessor.preprocess(data)

    userList = dataFrame['user'].unique().tolist()
    userList.remove('group_notification')
    userList.sort()
    userList.insert(0, 'Overall')

    selectedUser = streamlit.sidebar.selectbox('Show analysis of', userList)

    if streamlit.sidebar.button('Show Analysis'):
        numberOfMessages, numberOfWords, numberOfMediaMessages, numberOfLinks = helper.fetch_status(
            selectedUser, dataFrame)
        streamlit.title('Top Statistics')
        column1, column2, column3, column4 = streamlit.columns(4)

        with column1:
            streamlit.header('Total Messages')
            streamlit.title(numberOfMessages)
        with column2:
            streamlit.header('Total Words')
            streamlit.title(numberOfWords)
        with column3:
            streamlit.header('Media Shared')
            streamlit.title(numberOfMediaMessages)
        with column4:
            streamlit.header('Links Shared')
            streamlit.title(numberOfLinks)

        column1, column2 = streamlit.columns(2)
        with column1:
            streamlit.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selectedUser, dataFrame)
            fig, ax = pyplot.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            pyplot.xticks(rotation='vertical')
            streamlit.pyplot(fig)

        with column2:
            streamlit.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selectedUser, dataFrame)
            fig, ax = pyplot.subplots()
            ax.plot(daily_timeline['only_date'],
                    daily_timeline['message'], color='black')
            pyplot.xticks(rotation='vertical')
            streamlit.pyplot(fig)

        # activity map
        streamlit.title('Activity Map')
        column1, column2, column3 = streamlit.columns(3)

        with column1:
            streamlit.header("Most busy day")
            busy_day = helper.week_activity_map(selectedUser, dataFrame)
            fig, ax = pyplot.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            pyplot.xticks(rotation='vertical')
            streamlit.pyplot(fig)

        with column2:
            streamlit.header("Most busy month")
            busy_month = helper.month_activity_map(selectedUser, dataFrame)
            fig, ax = pyplot.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            pyplot.xticks(rotation='vertical')
            streamlit.pyplot(fig)

        with column3:
            streamlit.header("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selectedUser, dataFrame)
            fig, ax = pyplot.subplots()
            ax = seaborn.heatmap(user_heatmap)
            streamlit.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selectedUser == 'Overall':
            streamlit.title('Most Busy Users')
            x, new_dataFrame = helper.most_busy_users(dataFrame)
            fig, ax = pyplot.subplots()

            column1, column2 = streamlit.columns(2)

            with column1:
                ax.bar(x.index, x.values, color='red')
                pyplot.xticks(rotation='vertical')
                streamlit.pyplot(fig)

            with column2:
                streamlit.dataframe(new_dataFrame)

        column1, column2 = streamlit.columns(2)

        with column1:
            streamlit.title("Wordcloud")
            dataFrameWordCloud = helper.create_wordcloud(
                selectedUser, dataFrame)
            fig, ax = pyplot.subplots()
            ax.imshow(dataFrameWordCloud)
            streamlit.pyplot(fig)

        with column2:
            mostCommonDataFrame = helper.most_common_words(
                selectedUser, dataFrame)
            fig, ax = pyplot.subplots()

            ax.barh(mostCommonDataFrame[0], mostCommonDataFrame[1])
            pyplot.xticks(rotation='vertical')

            streamlit.title('Most common words')
            streamlit.pyplot(fig)

        # Emoji Analysis
        emoji_dataFrame = helper.emoji_helper(selectedUser, dataFrame)
        streamlit.title("Emoji Analysis")

        column1, column2 = streamlit.columns(2)

        with column1:
            streamlit.table(emoji_dataFrame)

        with column2:
            fig, ax = pyplot.subplots()
            ax.pie(emoji_dataFrame[1].head(), labels=emoji_dataFrame[0].head(), autopct="%0.2f")
            streamlit.pyplot(fig)

    else:
        streamlit.title('WhatsApp Analyser')

else:
    streamlit.title('WhatsApp Analyser')
