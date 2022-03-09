def gettotal(i):
    lambda i: i["mem"]+i["core"]

dict1 = {"id":1, "mem":0.2, "core": 0.4 }
dict2 = {"id":2, "mem":0.1, "core": 0.3 }
dict3 = {"id":3, "mem":0.5, "core": 0.6 }
dict4 = {"id":4, "mem":0.5, "core": 0.7 }
l = []
l.append(dict1)
l.append(dict2)
l.append(dict3)
l.append(dict4)
print(l)
del l[3]
print(l)
l.sort(reverse=True,key = lambda i: i["mem"]+i["core"])
print("sorted:")
print(l)


s = lambda k: l[0]["mem"]+l[0]["core"]
print(s(l))


