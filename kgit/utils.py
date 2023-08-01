
import json
import datetime
from itertools import islice
from typing import List
def chunked(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch

class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super(DateTimeEncoder, self).default(obj)

def build_option_string(options: List[str]) -> str:
    ret = ""
    c = ord("a")
    for i, option in enumerate(options):
        ret += f"({chr(c+i)}) {option}"
        if i != len(options) - 1:
            ret += " "
    return ret


def read_dataset(path: str):
    dataset = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            dataset.append(json.loads(line))
    return dataset

def write_dataset(path: str, dataset):
    with open(path, 'w', encoding='utf-8') as f:
        for obj in dataset:
            f.write(json.dumps(obj) + '\n')