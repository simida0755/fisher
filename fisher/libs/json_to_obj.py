
database = {
    'status': '0',
    'msg': 'ok',
    'result': {
        'number': '780098068058',
        'type': 'zto',
        'list': [
            {
                'time': '2018-03-09 11:59:26',
                'status': '【石家庄市】 快件已在 【长安三部】 签收,签收人: 本人, 感谢使用中通快递,期待再次为您服务!'
            },
            {
                'time': '2018-03-09 09:03:10',
                'status': '【石家庄市】快件已到达【长安三部】（0311-85344265）,业务员 容晓光（13081105270）正在第1次派件'
            },
            {
                'time': '2018-03-08 23:43:44',
                'status': '【石家庄市】 快件离开 【石家庄】 发往 【长安三部】'
            },
            {
                'time': '2018-03-08 21:00:44',
                'status': '【石家庄市】 快件到达 【石家庄】'
            },
            {
                'time': '2018-03-07 01:38:45',
                'status': '【广州市】 快件离开 【广州中心】 发往 【石家庄】'
            },
            {
                'time': '2018-03-07 01:36:53',
                'status': '【广州市】 快件到达 【广州中心】'
            },
            {
                'time': '2018-03-07 00:40:57',
                'status': '【广州市】 快件离开 【广州花都】 发往 【石家庄中转】'
            },
            {
                'time': '2018-03-07 00:01:55',
                'status': '【广州市】 【广州花都】（020-37738523） 的 马溪 （18998345739） 已揽收'
            }
        ],
        'deliverystatus': '3',
        'issign': '1',
        'expName': '中通快递',
        'expSite': 'www.zto.com',
        'expPhone': '95311',
        'courier': '容晓光',
        'courierPhone': '13081105270',
        'updateTime': '2019-08-27 13:56:19',
        'takeTime': '2天20小时14分',
        'logo': 'http://img3.fegine.com/express/zto.jpg'
    }
}
class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst =Dict()
    for k ,v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst

def complex_dict_to_object(Obj):
    if not (isinstance(Obj, dict) or isinstance(Obj, list)):
        return Obj
    inst = Dict()
    if isinstance(Obj, dict):
        for k, v in Obj.items():
            inst[k] = complex_dict_to_object(v)
        return inst
    if isinstance(Obj, list):
        obj_list = []
        for x in Obj:
            obj_list.append(complex_dict_to_object(x))
            # x = complex_dict_to_object(x)
        return obj_list


if __name__=='__main__':
    result =complex_dict_to_object(database)
    print(result.status)
    print(result.result.list)
    for x in result.result.list:
        print(x.time)
        print(x.status)
