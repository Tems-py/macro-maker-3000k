import os
import threading
import time
import keyboard
from pynput.mouse import Listener


def main():
    from macro import script, new

    if not os.path.isdir("saved"):
        os.mkdir("saved")
        print("Created saved folder")
        print("Please restart the program, press any key...")
        os.system('pause')
        exit()

    print("Loading scripts...")
    scripts = []
    for file in os.listdir("saved"):
        if file.endswith(".mkr"):
            scripts.append(script(file[:-4]))
    print("Loaded " + str(len(scripts)) + " scripts")
    print("")
    print("Available scripts:")
    for script in scripts:
        print(script.name)
    print("")
    print("Type 'exit' to exit")
    print("")
    print("Type 'new' to create a new script")
    print("")
    print("Type 'run' to run a script")
    print("")
    print("Type 'load' to load a script")
    print("")

    x = input("Enter command: ")
    while x != "exit":
        if x == "new":
            name = input("Enter script name: ")
            if name in [script.name for script in scripts]:
                print("Script already exists")
                continue
            print("Recording will start after you continue")
            time.sleep(0.1)
            os.system('pause')
            time_start = time.perf_counter()
            keys = []
            print("Press scroll lock to stop recording")

            def on_click(x_c, y_c, button, pressed):
                print([[x_c, y_c, button, pressed], time.perf_counter() - time_start])
                keys.append(["m", [x_c, y_c, str(button), pressed], time.perf_counter() - time_start])

            with Listener(on_click=on_click):
                while True:
                    key = keyboard.read_key()
                    if key == "scroll lock":
                        break
                    print([key, time.perf_counter() - time_start])
                    keys.append(["k", key, time.perf_counter() - time_start])
            print("Recording finished")
            print("")
            scripts.append(new(name, keys))

        elif x == "run":
            name = input("Enter script name: ")
            print("Running script...")
            print("")
            print("You can press scroll lock to stop the script")
            for script in scripts:
                if script.name == name:
                    thr = threading.Thread(target=script.run)
                    thr.start()
                    break

        elif x == "load":
            name = input("Enter script name: ")
            path = input("Enter script path: ")
            for script in scripts:
                if script.name == name:
                    print("Already exist")
                    os.system('pause')
                    exit()
            scripts.append(script(name, path))
            print("")
            y = input("Script loaded, would you like to create copy of it in saved folder? (y/n)")
            if y == "y":
                os.system("copy saved/" + name + ".mkr saved/" + name + "_copy.mkr")
                print("")
                print("Copy created")
                print("")
            else:
                print("")
        else:
            print("")
            print("Invalid command")
            print("")
        x = input("Enter command: ")


if __name__ == "__main__":
    print("MACRO CREATOR 5000K\n\n")
    threading.Thread(target=main).start()
