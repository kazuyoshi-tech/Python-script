from selenium import webdriver
from bs4 import BeautifulSoup
import chromedriver_binary
import pandas as pd

import os
import sys
import glob
import shutil
import time
import csv
import dateutil.parser

def csvDownload():
    url = "https://www.mhlw.go.jp/stf/covid-19/open-data.html"
    driver = webdriver.Chrome()

    try:
        # カレントディレクトリの取得
        current_dir = os.getcwd()

        # 一時ダウンロードフォルダパスの設定
        tmp_download_dir = f'{current_dir}/tmp_download'

        # 一時フォルダが存在していたら消す(前回のが残存しているかも)
        if os.path.isdir(tmp_download_dir):
            shutil.rmtree(tmp_download_dir)
        # 一時フォルダの作成
        os.mkdir(tmp_download_dir)
        
        # Chromeオプション設定でダウンロード先の変更
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : tmp_download_dir }
        options.add_experimental_option('prefs',prefs)

        # オプションを適用してChromeを起動
        driver = webdriver.Chrome(chrome_options = options)

        # Seleniumでダウンロード開始処理
        driver.get(url)
        # 単数要素をクリック方法
        #driver.find_element_by_class_name('m-link').click()
        # 複数要素取得後クリック
        CSVs = driver.find_elements_by_class_name('m-link')
        for CSV in CSVs:
            CSV.click()
        # 待機タイムアウト時間(秒)設定
        timeout_second = 10
        for i in range(timeout_second + 1):
            # 一秒待つ
            time.sleep(1)

            # # ファイル一覧取得
            # if download_fileName:
            #     download_fileName = glob.glob(f'{tmp_download_dir}\\*.*')
            #     # ファイルが存在する場合
            #     if download_fileName:
            #         # 拡張子の抽出
            #         extension = os.path.splitext(download_fileName[0])
            #         # 拡張子が '.crdownload' ではない ダウンロード完了 待機を抜ける
            #         if '.crdownload' not in extension[1] : break

        # Chromeを閉じる
        driver.quit()

        return True

        # 正ダウンロードフォルダへ格納
        # shutil.move(download_fileName[0], f'{current_dir}\\Download')
        # 一時フォルダの削除
        # shutil.rmtree(tmp_download_dir)
    except:
        print('CSVダウンロード失敗......')
        return False

def csvformater(file_path:str, head_flag:bool):
    tmp_download_dir = f'{os.getcwd()}/tmp_download'
    tmp_format_dir = f'{os.getcwd()}/tmp_format'

    # csv名取得
    file_name = file_path.replace(f'{tmp_download_dir}/','')

    format_data_path = f'{tmp_format_dir}/{file_name}'    

    with open(format_data_path, 'w') as w:
        writer = csv.writer(w)
        with open(file_path) as f:
            reader = csv.reader(f)
            # 配列化
            reader = [row for row in reader]

            # ヘッダーの取り出し
            header = reader[0]
            # ヘッダーを削除
            reader.pop(0)

            # ヘッダー書き込み
            if head_flag:
                writer.writerow(header)
            else:
                writer.writerow(header[1:])

            for row in reader:
                row[0] = dateutil.parser.parse(row[0]).strftime("%Y/%m/%d")
                if '2020/03/01' <= row[0]:
                    if head_flag:
                        writer.writerow(row)
                    else:
                        writer.writerow(row[1:])

def main():
    csvExist = True#csvDownload()
    if csvExist:
        # カレントディレクトリの取得
        current_dir = os.getcwd()
        # 一時ダウンロードフォルダパスの設定
        tmp_download_dir = f'{current_dir}/tmp_download'

        # 取得ファイル一覧取得(フルパスも含み)
        download_fileNames = glob.glob(f'{tmp_download_dir}/*.*')

        # 前回のCSVまとめファイルを削除
        ex_sumamy_data_path = f'{tmp_download_dir}/corona_summary_data.csv'
        if os.path.isdir(ex_sumamy_data_path):
            shutil.rmtree(ex_sumamy_data_path)
        # フォーマット用フォルダが存在していたら消す(前回のが残存しているかも)
        tmp_format_dir = f'{current_dir}/tmp_format'
        if os.path.isdir(tmp_format_dir):
            shutil.rmtree(tmp_format_dir)
        # フォーマット用フォルダの作成
        os.mkdir(tmp_format_dir)

        # # 取得ファイルの一覧作成(ファイル名のみ)
        # download_fileNames = []
        # for tmp_fileName in tmp_fileNames:
        #     # .replaceで不要パスを削除
        #     download_fileName = tmp_fileName.replace(tmp_download_dir+'/','')
        #     download_fileNames.append(download_fileName)

        csvfile_paths = [
            f'{tmp_download_dir}/pcr_positive_daily.csv',   # 陽性者数
            f'{tmp_download_dir}/pcr_tested_daily.csv',     # 検査実施件数
            f'{tmp_download_dir}/pcr_case_daily.csv',       # 調査機関場所
            f'{tmp_download_dir}/cases_total.csv',          # 入院必要者数
            f'{tmp_download_dir}/severe_daily.csv',         # 重傷者数
            f'{tmp_download_dir}/recovery_total.csv',       # 回復者
            f'{tmp_download_dir}/death_total.csv',          # 死者数
        ]

        # CSVファイルの整形
        head_flag = True
        for csvfile_path in csvfile_paths:
            if csvfile_path in csvfile_paths:
                csvformater(csvfile_path,head_flag)
                #csvMaker(csvfile_path,head_flag)
                head_flag = False

if __name__ == "__main__":
    main()