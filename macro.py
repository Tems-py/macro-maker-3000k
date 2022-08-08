import json
import os
import pyautogui
import time

import keyboard


class script:
    def __init__(self, name, path=None):
        self.name = name

        if path:
            self.file_path = path + name + '.mkr'
        else:
            self.file_path = "saved/" + name + '.mkr'

        if not os.path.isfile(self.file_path):
            raise Exception("File not found: " + self.file_path)

        with open(self.file_path, 'r') as f:
            self.script_json = json.load(f)

        self.author = self.script_json['author']
        self.steps = self.script_json['steps']
        self.latency_ms = self.script_json['latency_ms']

    def run(self):
        for step in self.steps:
            time.sleep(step[2])
            print(step)
            if step[0] == "k":
                keyboard.write(step[1])
            elif step[0] == "m":
                if step[1][3]:
                    pyautogui.click(step[1][0], step[1][1])



class new:
    def __init__(self, name, steps, latency=-1):
        self.name = name
        self.steps = steps
        self.latency_ms = latency
        self.file_path = "saved/" + name + '.mkr'

        self.author = os.getenv('USERNAME')

        steps_to_save = []
        for i in range(len(steps)):
            if i == 0:
                steps_to_save.append([steps[i][0], steps[i][1], 0])
            else:
                steps_to_save.append([steps[i][0], steps[i][1], steps[i][2] - steps[i - 1][2]])

        print(steps_to_save)

        self.script_json = {
            "author": "",
            "steps": steps_to_save,
            "latency_ms": latency
        }

        with open(self.file_path, 'w') as f:
            json.dump(self.script_json, f)
