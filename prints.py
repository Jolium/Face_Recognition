import settings as sets


def prints(video):
    dic = sets.dict_properties

    for k, v in dic.items():
        value = video.get(v)
        if value != -1.0:
            print(f'{k} ({v}):  {value}')
