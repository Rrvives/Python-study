import json

data = [{"a": "测试"}]
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)
data1 = '[{"a": "测试"}]'
l = json.loads(data1)
print(l)