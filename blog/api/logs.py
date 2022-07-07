import json
from datetime import timedelta

from blog.api.redis_helper import redis_helper
from blog.models import Log

client = redis_helper()


def add_log(user, post_datetime, message, method):
    logs = client.get('logs')
    logs_dict = {}
    if logs is not None:
        logs_dict = json.loads(logs)

    if logs_dict is None:
        # non sono ancora stati creati log
        logs_dict = {}

    day = post_datetime.strftime("%d/%m/%Y")
    if day in logs_dict:
        today_logs = logs_dict[day]
    else:
        today_logs = {}

    current_hour = post_datetime.strftime("%H")
    if current_hour in today_logs:
        hour_logs = today_logs[current_hour]
        hour_logs = list(filter(lambda x: x['user'] == user, hour_logs))
    else:
        hour_logs = []

    if hour_logs is None:
        # scattata nuova ora, scrivo su sqlLite i log precedenti se ci sono
        prev_hour = post_datetime.hour - timedelta(hours=1)
        prev_hour_string = prev_hour.strftime('%H')
        if prev_hour_string in today_logs:
            prev_logs = today_logs[prev_hour_string]

        if prev_logs is not None:
            post_list = list(filter(lambda x: x['method'] == 'POST', prev_logs))
            put_list = list(filter(lambda x: x['method'] == 'PUT', prev_logs))
            delete_list = list(filter(lambda x: x['method'] == 'DELETE', prev_logs))
            log = ''
            if len(post_list) > 0:
                log = Log(message=f'Dalle {prev_hour} alle {post_datetime.hour} {user} ha creato {len(post_list)} post')

            if len(put_list) > 0:
                log = Log(message=f'Dalle {prev_hour} alle {post_datetime.hour} {user} ha modificato {len(put_list)} post')

            if len(delete_list) > 0:
                log = Log(
                    message=f'Dalle {prev_hour} alle {post_datetime.hour} {user} ha eliminato {len(delete_list)} post')

            log.date = post_datetime.day
            log.save()

    hour_logs.append({'time': post_datetime.strftime('%H:%M'), 'message': message, 'method': method, 'user': user})
    today_logs[post_datetime.strftime('%H')] = hour_logs

    logs_dict[post_datetime.strftime("%d/%m/%Y")] = today_logs
    client.set('logs', json.dumps(logs_dict))
