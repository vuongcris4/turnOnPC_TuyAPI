#  pyinstaller --onefile -w tuya.py -i tuya.ico

import tkinter as tk
import tinytuya
from os import path
import time 

CONFIG_FILE = path.expandvars(r"%appdata%/config_tuya_api.ini")

API_REGION = "us"
API_KEY = "ppha8pvgsdmykpfy5wwk"
API_SECRET = "94f49077f34c47aab31369fadeccaa10"
DEVICE_ID = "eb9f19eca7f66c46b10dam"

root = tk.Tk()
label_status = tk.Label(root, text="", font=("Arial", 17))
label_status.pack()

# pressed_setting_button = False

def read_config_file():
    try:
        f = open(CONFIG_FILE, "r")
        api_read = f.read().split("\n")
        global API_REGION, API_KEY, API_SECRET, DEVICE_ID
        API_REGION = api_read[0]
        API_KEY = api_read[1]
        API_SECRET = api_read[2]
        DEVICE_ID = api_read[3]
        f.close()
    except IOError:    # this is what happens if the file doesn't exist
        f = open(CONFIG_FILE, "w")
        f.write(API_REGION + "\n" + API_KEY +
                "\n" + API_SECRET + "\n" + DEVICE_ID)
        f.close()


def run():
    c = tinytuya.Cloud(apiRegion=API_REGION,
                       apiKey=API_KEY,
                       apiSecret=API_SECRET,
                       )
    id = DEVICE_ID

    # Send Command - Turn on switch
    commands = {
        "commands": [
            {
                "code": "switch_1",
                "value": True
            },
        ]
    }

    # print("Turning on PC...")
    result = c.sendcommand(id, commands)
    try:
        if (result['success']):
            label_status.config(text="Turn on pc SUCCESS")
        else:
            label_status.config(text="CAN't turn on PC")
    except:
        label_status.config(text="CAN't turn on PC")


def save_config(top, entries):
    try:
        f = open(CONFIG_FILE, "w")
        result = ""
        for entry in entries:
            result += entry[1].get() + "\n"
        f.write(result)
        f.close()
        read_config_file()
        run()
        top.destroy()

    except:    # this is what happens if the file doesn't exist
        tk.messagebox.showerror("Error", "Error when save file")


def makeform(root, fields, data_entries):
    entries = []
    for field, data in zip(fields, data_entries):
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, data)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries


def popup_setting():
    # global pressed_setting_button
    # pressed_setting_button = True

    top = tk.Toplevel(root)
    w = 400
    h = 160
    top.geometry('%dx%d+%d+%d' % (w, h, (ws/2) - (w/2), (hs/2) + 70))
    top.title("Config TuyaAPI (turn on device) by vuongcris4")

    fields = ['API_REGION', 'API_KEY', 'API_SECRET', 'DEVICE_ID']
    data_entries = [API_REGION, API_KEY, API_SECRET, DEVICE_ID]
    ents = makeform(top, fields, data_entries)

    tk.Button(top, text='SAVE and RUN', command=(
        lambda e=ents: save_config(top, e))).pack(ipadx=5,
                                                  ipady=5,
                                                  expand=True)


if __name__ == "__main__":
    read_config_file()

    w = 250
    h = 70
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' % (w, h, (ws/2) - (w/2), (hs/2) - (h/2)))
    root.resizable(False, False)
    root.title('Turn on PC')

    tk.Button(
        root,
        text="Config API",
        command=popup_setting
    ).pack(
        ipadx=5,
        ipady=5,
        expand=True
    )

    run()

    # time.sleep(2000)
    # root.after(3000, root.destroy)
    root.mainloop()

