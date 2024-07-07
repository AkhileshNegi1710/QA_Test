import subprocess
import os
import time
import requests

def runTerminal(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    print(out.decode())
    if err:
        print(err.decode())
    return process.returncode

def getServiceIP(service_name):
    command = f"kubectl get service {service_name} --output=jsonpath='{{.spec.clusterIP}}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(err.decode())
        return None
    return out.decode().strip()

def validateAPIs(endpoint, expected_status):
    try:
        response = requests.get(endpoint)
        if response.status_code == expected_status:
            print(f"API {endpoint} is working as expected.")
            return True
        else:
            print(f"API {endpoint} returned status code {response.status_code}. Expected {expected_status}.")
            return False
    except requests.RequestException as e:
        print(f"API {endpoint} test failed with exception: {e}")
        return False

def main():
    print("Starting Minikube command")
    if runTerminal("minikube start --driver=docker") != 0:
        print("Failed to start Minikube.")
        return

    time.sleep(10)
    # --> add path where frontend.yaml and backend.yaml files are presnet
    os.chdir("D:\\QA-test\\Deployment")

    print("backend deployment command")
    if runTerminal("kubectl apply -f backend-deployment.yaml") != 0:
        print("some error in backend deployment.")
        return

    print("frontend deployment command")
    if runTerminal("kubectl apply -f frontend-deployment.yaml") != 0:
        print("Some error in frontend deployment.")
        return
    print("Pods are getting ready")
    while True:
        status = subprocess.check_output("kubectl get pods", shell=True).decode()
        print(status)
        if "Running" in status:
            print("Please wait ---> all services should in running status")
            time.sleep(30)
            break
        time.sleep(5)
    frontend_service_ip = getServiceIP("frontend-service")
    backend_service_ip = getServiceIP("backend-service")
    if not frontend_service_ip or not backend_service_ip:
        print("Failed to get FrontEnd/Backend IPs.")
        return
    api_tests = [
        {"endpoint": f"http://{frontend_service_ip}:80/api/frontend", "expected_status": 200},
        {"endpoint": f"http://{backend_service_ip}:3000/api/backend", "expected_status": 200}
    ]
    Check_test = True
    for test in api_tests:
        if not validateAPIs(test["endpoint"], test["expected_status"]):
            Check_test = False


    if Check_test:
        print("All API tests passed. All services are running")
    else:
        print("Some API tests failed. Need to check logs")

if __name__ == "__main__":
    main()
