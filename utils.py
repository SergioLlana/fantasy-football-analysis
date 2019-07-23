import json
import csv


def read_json(path):
    return json.loads(read(path))


def read(path):
    with open(path, 'r') as f:
        return f.read()


def write_line(path, line):
    with open(path, 'a') as f:
        f.write_line(line)


def write_csv(path, content):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(content)
