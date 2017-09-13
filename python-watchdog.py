import os
import json
import time
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from stackMap.node import Node

CONFIG_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/config.json'


def main():
    with open(CONFIG_FILE_PATH) as configFile:
        config = json.load(configFile)

    if config:
        start_monitoring(config)
    else:
        print("Can't load configuration information")


def start_monitoring(config):
    observer = Observer()
    observer.schedule(MyHandler(config), config['directoryToWatch'], recursive=False)
    observer.start()
    print("Starting File System Watcher...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.log"]

    def __init__(self, config):
        PatternMatchingEventHandler.__init__(self)
        self.coalesced_node = None
        self.content = ""
        self.nodes = {}
        self.config = config
        self.counter = 0

    def on_modified(self, event):
        with open(event.src_path) as in_file:
            root_node = self.parse_file_to_nodes(in_file)
        if root_node is None:
            return
        self.write_node_to_file(root_node)

    def write_node_to_file(self, root_node):
        out_name = "out/eventOut{0}.json".format(self.counter)
        self.counter += 1
        with open(out_name, "w") as event_out_file:
            json.dump(root_node, event_out_file, indent=4)
        self.coalesced_node = Node.merge_nodes(self.coalesced_node, root_node)
        coalesced_name = "out/coalesced.json"
        with open(coalesced_name, "w") as coalesced_file:
            json.dump(self.coalesced_node, coalesced_file, indent=4)

    def parse_file_to_nodes(self, file):
        content = file.read()
        if self.content == content:
            return None
        self.content = content
        splitlines = content.splitlines()
        splitlines.reverse()
        root = Node("root")
        previous = root
        for line in splitlines:
            try:
                current = self.parse_line_to_node(line)
                previous.add_child(current)
                previous = current
            except IndexError:
                pass
        return root

    @staticmethod
    def parse_line_to_node(line):
        one = line.split("(")[0].split(".")
        name = one[-2] + "#" + one[-1]
        return Node(name)


if __name__ == '__main__':
    main()
