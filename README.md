# QA_Test

**Problem Statement 1: **
1. Run using ->  python QA_run.py
Please deploy below package using 
pip install subprocess
pip install os
pip install time
pip install requests 


Keep this script inside the Deployment folder where frontend and backend.yaml file is present
you can increase memory of minikube using below command if it is failing:
minikube start --cpus=4 --memory=8192



**Problem Statement 2: **
1. cpu_check.py checks CPU, Memory, Disk, and Process. The default threshold is 80, if it crosses the threshold then it will give an alert in the terminal and in the log file as well with current time.
   
2. application_check.py checks application is running or not through its status code.


