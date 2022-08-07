import requests
from datetime import datetime as dt
from LINE_Notify.line_notify import Linenotify


def get_stage_info_list() -> dict:
    url = 'https://spla2.yuu26.com/schedule'
    response = requests.get(url)
    result_json = {}
    if response.status_code == 200:
        response_json = response.json()
        result_json['status'] = 1
        result_json['result'] = response_json
    else:
        result_json['status'] = 0
        result_json['result'] = 'エラー'

    return result_json


# データを加工する関数（不要データの削除）
def process_data(stage_info_list, rule_filter) -> dict:
    result = list()
    for stage_info in stage_info_list:
        rule = stage_info['rule']
        # もしも望んだルールでなければ非表示にする
        if rule not in rule_filter:
            continue
        start_time = stage_info['start']
        end_time = stage_info['end']
        start_time = dt.strptime(start_time, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')
        end_time = dt.strptime(end_time, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')
        map1 = stage_info['maps'][0]
        map2 = stage_info['maps'][1]
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


if __name__ == '__main__':
    stage_info_list = get_stage_info_list()

    if stage_info_list['status'] == 1:
        regular_stage_info = stage_info_list['result']['result']['regular']
        gachi_stage_info = stage_info_list['result']['result']['gachi']
        league_stage_info = stage_info_list['result']['result']['league']
        # msg = create_send_stage_info(stage_info_list['result'])
    # else:
    #     msg = stage_info_list['stage_info_list']

    rule_filter = ['ガチヤグラ', 'ガチホコバトル']
    gachi_stage_info = process_data(gachi_stage_info, rule_filter)
    gachi_stage_info = create_msg_data(gachi_stage_info)

    # regular_stage_info = json.dumps(obj=regular_stage_info, indent=2, ensure_ascii=False)
    # gachi_stage_info = json.dumps(obj=gachi_stage_info, indent=2, ensure_ascii=False)
    # league_stage_info = json.dumps(obj=league_stage_info, indent=2, ensure_ascii=False)

    line_notify_obj = Linenotify('')
    # line_notify_obj.message = 'ナワバリバトル\n' + regular_stage_info
    # line_notify_obj.send_line_notify()
    line_notify_obj.message = '\nガチマッチ\n' + gachi_stage_info
    line_notify_obj.send_line_notify()
    # line_notify_obj.message = 'リーグマッチ\n' + league_stage_info
    # line_notify_obj.send_line_notify()
