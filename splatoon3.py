import requests
from datetime import datetime as dt
from LINE_Notify.line_notify import Linenotify


def get_stage_info_list() -> dict:

    url = 'https://spla3.yuu26.com/api/schedule'
    """ 
    splatoon 3 API
    https://spla3.yuu26.com/
    """
    response = requests.get(url)
    result_json = {}
    if response.status_code == 200:
        response_json = response.json()
        result_json['status'] = 1
        result_json['result'] = response_json['result']
    else:
        result_json['status'] = 0
        result_json['result'] = 'エラー'

    return result_json


# データを加工する関数（不要データの削除）
def process_data(stage_info_list) -> dict:
    result = list()
    for stage_info in stage_info_list:
        rule = stage_info['rule']['name']
        start_time = stage_info['start_time']
        end_time = stage_info['end_time']
        start_time = dt.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
        end_time = dt.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
        map1 = stage_info['stages'][0]['name']
        map2 = stage_info['stages'][1]['name']
        value = {
            'start_time_end_time': f'{start_time} ～ {end_time}',
            'rule': f'\t{rule}',
            'map1': f'\t\t{map1}',
            'map2': f'\t\t{map2}',
        }
        result.append(value)
        # print(stage_info)
    return result


def create_msg_data(processing_data_list) -> str:
    result = ''
    for processing_data in processing_data_list:
        result += '\n'
        for v in processing_data.values():
            result += f'{v}\n'
    return result


def main():
    stage_info_list = get_stage_info_list()
    line_notify_obj = Linenotify('')

    if stage_info_list['status'] == 0:
        message = 'API 取得エラー'
    elif stage_info_list['status'] == 1:
        x_stage_info = stage_info_list['result']['x']
        # regular_stage_info = stage_info_list['result']['regular']
        # league_stage_info = stage_info_list['result']['league']

        x_stage_info = process_data(x_stage_info)
        x_stage_info = create_msg_data(x_stage_info)
        message = '\nXマッチ\n' + x_stage_info
    line_notify_obj.message = message
    line_notify_obj.send_line_notify()
    # line_notify_obj.message = 'リーグマッチ\n' + league_stage_info
    # line_notify_obj.send_line_notify()


if __name__ == '__main__':
    main()
