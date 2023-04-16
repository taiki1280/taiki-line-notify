from distutils.spawn import spawn
import splatoon3

# 00 ライブラリをインポート
import schedule
from time import sleep


# 01 定期実行する関数を準備
def task():
    # print('aaa')
    splatoon3.main()


# 02 スケジュール登録
schedule.every().day.at("12:00").do(task)
# schedule.every(0.4).seconds.do(task)


# 03 イベント実行
while True:
    schedule.run_pending()
    sleep(1)
