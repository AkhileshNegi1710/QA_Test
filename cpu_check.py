import psutil
import logging
import time

logging.basicConfig(filename="logFile.log", level=logging.INFO,
                    format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# keeping all threshold as 80
cpu_threshold = 80
memory_threshold = 80
disk_threshold = 80

def consoleLog(message):
    print(message)
    logging.info(message)

def checkCPU():
    cpuUsage = psutil.cpu_percent(interval=1)
    # print(cpuUsage)
    if cpuUsage > cpu_threshold:
        consoleLog(f"CPU ALERT: High CPU usage detected: {cpuUsage}%")

def checkMemory():
    memory = psutil.virtual_memory()
    memoryUsage = memory.percent
    # print(type(memoryUsage))
    # total_memory = memory.total
    if memoryUsage > memory_threshold:
        consoleLog(f"MEMORY ALERT: High memory usage detected: {memoryUsage}%")

def checkDisk():
    disk = psutil.disk_usage("/")
    # print("checking disk",disk)
    diskUsage = disk.percent
    if diskUsage > disk_threshold:
        consoleLog(f"ALERT: High disk usage detected: {diskUsage}%")

def checkProcesses():
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        cpuUsage = proc.info["cpu_percent"]
        memoryUsage = proc.info["memory_percent"]
        if cpuUsage > cpu_threshold or memoryUsage > memory_threshold:
            consoleLog(f"PROCESS ALERT: High resource usage detected for process {proc.info["name"]} (PID: {proc.info["pid"]}) "
                      f"CPU: {cpuUsage}%, Memory: {memoryUsage}%")




if __name__ == "__main__":
    consoleLog("Starting System Check: ")
    while True:
        checkCPU()
        checkMemory()
        checkDisk()
        checkProcesses()
        time.sleep(60)
