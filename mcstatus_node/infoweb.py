# coding: utf-8

import os
import sys
import json
import shlex
from bottle import route, run, template, response, abort, default_app
from subprocess import PIPE, Popen

def run_cmd(cmd):
    p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return stdout

@route('/')
def info():
    response.content_type = 'text/json'
    memory = get_memory()
    cpu = get_cpus()
    load = get_load()
    
    data = {
        "memory": int(memory["memory"]),
        "memory_max": int(memory["memory_max"]),
        "cpu_count": cpu["cpu_count"],
        "load1": load[0],
        "load5": load[1],
        "load15": load[2],
        "port": get_port(),
    }
    return json.dumps(data, indent=4)

def get_port():
    port = 0
    try:
        paths = (
            "/home/bukkit/server.properties",
            "/home/minecraft/game/server.properties",
            "/home/minecraft/server.properties",
            "/home/tekkit/server.properties",
            "/home/tekkit_lite/server.properties",
        )
        existed_path = None
        for path in paths:
            if os.path.isfile(path):
                existed_path = path
                break
        if existed_path:
            with open(existed_path) as f:
                for line in f.readlines():
                    if "server-port" in line:
                        port = int(line.strip().split("=")[1])
    except IOError:
        pass
    return port

def get_load():
    data = (0.0, 0.0, 0.0)
    try:
        output = run_cmd("uptime").strip()
    except IOError:
        pass
    if len(output.split(" ")) > 3:
        load1m = float(output.split(" ")[-1].strip(" ,").replace(",", "."))
        load5m = float(output.split(" ")[-2].strip(" ,").replace(",", "."))
        load15m = float(output.split(" ")[-3].strip(" ,").replace(",", "."))
        data = (load1m, load5m, load15m)
    return data

def get_memory():
    output = {"memory": 0, "memory_max": 0}
    try:
        data = [x.strip().split() for x in run_cmd("free -m").split("\n")]
        output["memory_max"] = data[1][1]
        output["memory"] = data[2][2]
    except IOError:
        pass
    return output

def get_cpus():
    data = {"cpu_count": 1}
    try:
        output = run_cmd("cat /proc/cpuinfo").strip()
    except IOError:
        output = ""
    if output:
        cpus = []
        for x in [x.strip() for x in output.split("\n")]:
            if "processor" in x:
                cpus.append(int(x.split()[2].strip()))
        data["cpu_count"] = max(cpus)+1 if cpus else 1
    return data

def main():
    run(host='0.0.0.0', port=4999)

if __name__ == "__main__":
     main()
else:
     application = default_app()
