import re
import pandas


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dataFrame = pandas.DataFrame({'user_message': messages, 'message_date': dates})
    dataFrame['message_date'] = pandas.to_datetime(dataFrame['message_date'], format='%d/%m/%y, %H:%M - ')

    dataFrame.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in dataFrame['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(' '.join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    dataFrame['user'] = users
    dataFrame['message'] = messages
    dataFrame.drop(columns=['user_message'], inplace=True)

    dataFrame['only_date'] = dataFrame['date'].dt.date
    dataFrame['year'] = dataFrame['date'].dt.year
    dataFrame['month_number'] = dataFrame['date'].dt.month
    dataFrame['month'] = dataFrame['date'].dt.month_name()
    dataFrame['day'] = dataFrame['date'].dt.day
    dataFrame['day_name'] = dataFrame['date'].dt.day_name()
    dataFrame['hour'] = dataFrame['date'].dt.hour
    dataFrame['minute'] = dataFrame['date'].dt.minute

    period = []
    for hour in dataFrame[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    dataFrame['period'] = period

    return dataFrame
