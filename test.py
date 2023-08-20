from LINE_Notify.line_notify import Linenotify

def main():
    message = 'スプラ3 ステージ情報配信は止めました。'

    line_notify_obj = Linenotify('')
    line_notify_obj.message = message
    line_notify_obj.send_line_notify()

if __name__ == '__main__':
    main()
