import json

class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__



def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst



if __name__=='__main__':
    pass
