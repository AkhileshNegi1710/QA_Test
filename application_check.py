import requests
import logging
import time

session = requests.Session()

# Configuration
APP_URL = "https://takeuforward.org/"
logging.basicConfig(filename="checkStatusCode.log", level=logging.INFO,
                    format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def printLogger(message):
    print(message)
    logging.info(message)

def ValidateApplication():
    try:
        response = session.get(APP_URL, timeout=10)
        # print(response)
        if response.status_code == 200:
            printLogger(f"Application is UP. Status Code: {response.status_code}")
        else:
            printLogger(f"Application is DOWN. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        printLogger(f"Application is DOWN. Error: {e}")

if __name__ == "__main__":
    printLogger("Checking Application Status")
    while True:
        ValidateApplication()
        time.sleep(60)
