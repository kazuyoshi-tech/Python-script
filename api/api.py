from urllib.request import Request, urlopen
import json
import csv
from datetime import datetime as dt
import traceback
import os
import asyncio

def get_api(url:str) -> dict:
    req = Request(url)
    with urlopen(req) as res:
        body = json.load(res)
        return body

    
async def csv_proble_writer(problem_list:object):
    with open('./yukicoderProblem.csv', 'a') as f:
        problem_list = sorted(problem_list, key=lambda x:x['No'])
        headFlag = True
        for value in problem_list:
            tmp_dick = {}
            for key, val in value.items():
                if key == 'Statistics':
                    continue
                try:
                    if key == 'Date':
                        val = dt.fromisoformat(val[:-15])
                        val = val.strftime('%Y-%m-%d')
                    tmp_dick[key] = val
                except:
                    #traceback.print_exc()
                    #print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーー")
                    continue

            try:
                writer = csv.DictWriter(f, tmp_dick)
                if os.stat("./yukicoderProblem.csv").st_size == 0 and headFlag:
                    writer.writeheader()
                    headFlag = False
                writer.writerow(tmp_dick)
            except:
                print("書き込み失敗")
    print("問題書き込み終了！！")


async def csv_pass_contest_writer(pass_contest_list:object):
    with open('./yukicoderPassContest.csv', 'a') as f:
        pass_contest_list = sorted(pass_contest_list, key=lambda x:x['Id'])
        headFlag = True
        for value in pass_contest_list:
            tmp_dick = {}
            for key, val in value.items():
                try:
                    if key == 'Date' or key == 'EndDate':
                        val = dt.fromisoformat(val[:-15])
                        val = val.strftime('%Y-%m-%d')
                    tmp_dick[key] = val
                except:
                    #traceback.print_exc()
                    #print("ーーーーーーーーーーーーーーーーーーーーーーーーーーーー")
                    pass

            try:
                writer = csv.DictWriter(f, tmp_dick)
                if os.stat("./yukicoderPassContest.csv").st_size == 0 and headFlag:
                    writer.writeheader()
                    headFlag = False
                writer.writerow(tmp_dick)
            except:
                print("書き込み失敗")
    print("コンテスト書き込み終了！！")



YUKICODER_PROBLEM_URL = 'https://yukicoder.me/api/v1/problems/'
YUKICODER_PASS_CONTEST_URL = 'https://yukicoder.me/api/v1/contest/past'

result_problems = get_api(YUKICODER_PROBLEM_URL)
result_pass_contests = get_api(YUKICODER_PASS_CONTEST_URL)

#並列処理のインスタンス宣言
loop = asyncio.get_event_loop()

#並列処理するメソッドを指定
gather = asyncio.gather(
    csv_proble_writer(result_problems),
    csv_pass_contest_writer(result_pass_contests),
)

#実行
loop.run_until_complete(gather)

