from collections import Counter
from pathlib import Path

import emoji
import pandas
from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()


def fetch_status(selectedUser, dataFrame):
    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]
    numberOfMessages = dataFrame.shape[0]

    words = list()
    links = list()

    for message in dataFrame['message']:
        words.extend(message.split())

    numberOfMediaMessages = dataFrame[dataFrame['message'] == '<Media omitted>\n'].shape[0]

    for message in dataFrame['message']:
        links.extend(extract.find_urls(message))

    return numberOfMessages, len(words), numberOfMediaMessages, len(links)


def most_busy_users(dataFrame):
    user = dataFrame['user'].value_counts().head()
    dataFrame = round((dataFrame['user'].value_counts() / dataFrame.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return user, dataFrame


def create_wordcloud(selectedUser, dataFrame):
    with open(f'{Path(__file__).parent}\stop_english.txt') as file:
        stopWords = file.read()

    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]

    temporary = dataFrame[dataFrame['user'] != 'group_notification']
    temporary = temporary[temporary['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stopWords:
                words.append(word)
        return " ".join(words)

    wordCloud = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temporary['message'] = temporary['message'].apply(remove_stop_words)
    dataFrameOfWordCloud = wordCloud.generate(temporary['message'].str.cat(sep=" "))
    return dataFrameOfWordCloud


def most_common_words(selectedUser, dataFrame):
    with open(f'{Path(__file__).parent}\stop_english.txt') as file:
        stopWords = file.read()

    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]

    temporary = dataFrame[dataFrame['user'] != 'group_notification']
    temporary = temporary[temporary['message'] != '<Media omitted>\n']

    words = list()
    for message in temporary['message']:
        for word in message.lower().split():
            if word not in stopWords:
                words.append(word)

    mostCommonDataFrame = pandas.DataFrame(Counter(words).most_common(30))
    return mostCommonDataFrame


def emoji_helper(selectedUser, dataFrame):
    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]

    emojis = list()
    for message in dataFrame['message']:
        emojis.extend([char for char in message if char in emoji.UNICODE_EMOJI['en']])

    emojiDataFrame = pandas.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojiDataFrame


def monthly_timeline(selectedUser, dataFrame):
    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]

    timeline = dataFrame.groupby(['year', 'month_number', 'month']).count()['message'].reset_index()

    time = list()
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selectedUser, dataFrame):
    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]
    dailyTimeline = dataFrame.groupby('only_date').count()['message'].reset_index()
    return dailyTimeline


def week_activity_map(selectedUser, dataFrame):
    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]
    return dataFrame['day_name'].value_counts()


def month_activity_map(selectedUser, dataFrame):
    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]
    return dataFrame['month'].value_counts()


def activity_heatmap(selectedUser, dataFrame):
    if selectedUser != 'Overall':
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]
    userHeatMap = dataFrame.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return userHeatMap
