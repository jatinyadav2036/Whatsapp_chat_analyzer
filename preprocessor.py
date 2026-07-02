import pandas as pd
import re

def preprocess (data):
    pattern = r"(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}\s?[ap]m) - (.*)"

    matches = re.findall(pattern, data)

    df1 = pd.DataFrame(matches, columns=["Date", "Time", "Message"])

    df1["Datetime"] = pd.to_datetime(df1["Date"] + " " + df1["Time"], format="%d/%m/%y %I:%M %p")

    df1 = df1[['Datetime', 'Message']]

    df1 = df1.copy()

    users = []
    texts = []

    for msg in df1["Message"]:
        if ": " in msg:
            user, text = msg.split(": ", 1)
        else:
            user = None
            text = msg
        users.append(user)
        texts.append(text)

    df1["User"] = users
    df1["message"] = texts
    df1 = df1[["Datetime", "User", "message"]]

    df1['year'] = df1['Datetime'].dt.year
    df1['day_name'] = df1['Datetime'].dt.day_name()
    df1['month_name'] = df1['Datetime'].dt.month_name()
    df1['month'] = df1['Datetime'].dt.month_name()
    df1['month_num'] = df1['Datetime'].dt.month
    df1['date'] = df1['Datetime'].dt.date
    df1['day'] = df1['Datetime'].dt.day
    df1['minute'] = df1['Datetime'].dt.minute
    df1['hour'] = df1['Datetime'].dt.hour

    period = []
    for hour in df1[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df1['period'] = period

    return df1