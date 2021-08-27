import pymysql.cursors
import json
from datetime import date, datetime
import requests
import asyncio

# Connect to the database
connection = pymysql.connect(host='',
    user='',
    password='',
    database='scoreserver',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

async def default(o):
    #if isinstance(o, (datetime, date)):
    #    return o.isoformat()
    if hasattr(o,"isoformat"):
        return o.isoformat()
    return o

def send_slack(line):
    text = f'{line["created_at"].strftime("%m月%d日%H時%M分")}' + f'<https://contest.ictsc.net/#/manage/problems/{line["id"]}/answers|' + f'問題名:{line["title"]}({line["code"]})' + f' チーム名:{line["name"]}>' + "\n"
    payload={"text": text}
    response = requests.post("https://hooks.slack.com/services/",data=json.dumps(payload))
    print(f'{response.status_code} {response.text}')

result = []

with connection:
    with connection.cursor() as cursor:
        sql = "SELECT answers.id, answers.created_at, problems.code, problems.title, user_groups.name FROM answers INNER JOIN problems ON answers.problem_id = problems.id INNER JOIN user_groups ON answers.user_group_id = user_groups.id WHERE NOW() > ( answers.created_at + INTERVAL 15 MINUTE ) AND answers.point IS NULL ORDER BY answers.updated_at;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for line in result:
            send_slack(line)
