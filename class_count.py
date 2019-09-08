import json
import sys
from collections import defaultdict
from html.parser import HTMLParser


classes = defaultdict(int)


class ClassCounter(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for (attr, val) in attrs:
            if attr == 'class':
                classes[val] += 1


parser = ClassCounter()

try:
    with open(sys.argv[1], 'r') as f:
        parser.feed(f.read())
    print(json.dumps(classes, indent = 4))
except Exception as e:
    print(e)
