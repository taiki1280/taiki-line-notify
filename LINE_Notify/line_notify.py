import LINE_Notify.config as config
import requests


class Linenotify:
    def __init__(self,  message: str):
        self.message = message

    def send_line_notify(self) -> None:
        """
        LINE へ通知をする関数
        """
        if config.LINE_NOTIFY_TOKEN == None:
            print('環境変数「LINE_NOTIFY_TOKEN」を設定してください。')
            print('\t例）「.env.exampale」をご参考にしてください。')
            return
        API_URL = 'https://notify-api.line.me/api/notify'
        data = {'message': f'message: {self.message}'}
        headers = {'Authorization': f'Bearer {config.LINE_NOTIFY_TOKEN}'}
        response = requests.post(url=API_URL, headers=headers, data=data)
        if response.status_code == 200:
            print('下記のメッセージを送信したよ！\n')
            print(self.message)
        else:
            print('送信できなかったぞ？')
