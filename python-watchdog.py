import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

CONFIG_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/config.json'


def main():
    with open(CONFIG_FILE_PATH) as configFile:
        config = json.load(configFile)

    if config:
        startMonitoring(config)
    else:
        print(
            "Can't load configuration information. Check config.json in this directory for typos. If config.json does "
            "not exist, that's the problem.")


def startMonitoring(config):
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
        self.nodes = []
        self.config = config
        self.counter = 0

    def on_modified(self, event):
        self.do_something(event)
        with open("out/eventOut{0}.json".format(self.counter), "w") as event_out_file:
            self.counter += 1
            print(self.counter)
            json.dump(self.nodes, event_out_file, indent=4)

    def on_created(self, event):
        print("[Sending Email] Created: %s" % (event.src_path))
        self.do_something(event)

    def on_moved(self, event):
        pass

    def on_deleted(self, event):
        pass

    def do_something(self, event):
        with open(event.src_path) as f:
            # content = f.read()
            for line in f:
                self.parse_line_to_node(line)

    def parse_line_to_node(self, line):
        one = line.split("(")[0].split(".")
        try:
            class_and_method = one[-2] + "#" + one[-1]
            self.nodes.append(class_and_method)
        except IndexError:
            pass

if __name__ == '__main__':
    main()
