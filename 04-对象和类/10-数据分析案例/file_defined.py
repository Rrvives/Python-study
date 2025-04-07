# 定义一个抽象类
import json

from data_define import Record
class FileRender:
    def read_adta(self) -> list:
        pass


class TextFileRender(FileRender):
    def __init__(self, path):
         self.path = path

    def read_data(self):
        file = open(self.path, 'r', encoding='utf-8')
        record_list = []
        for line in file.readlines():
            line = line.strip() #去掉换行
            data_list = line.split(',')
            record = Record(data_list[0], data_list[1], int(data_list[2]), data_list[3])
            record_list.append(record)
        file.close()
        return record_list

class JsonFileRender(FileRender):
    def __init__(self, path):
        self.path = path

    def read_data(self):
        file = open(self.path, 'r', encoding='utf-8')
        record_list = []
        for line in file.readlines():
            record = json.loads(line)
            record = Record(record['date'], record['order_id'], record['money'], record['province'])
            record_list.append(record)
        file.close()
        return record_list

if __name__ == '__main__':
    render_text = TextFileRender('1月.txt')
    render_json = JsonFileRender('2月.txt')
    list1 = render_text.read_data()
    list2 = render_json.read_data()
    for l in list1:
        print(l)

    for l in list2:
        print(l)