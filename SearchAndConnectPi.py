"""
ESP- Este codigo escanea todas las raspberry conectadas a la red y manda un archivo a cada una de ellas sobre SSH
ENG- Scan all IP connected in the local network and detect all the Raspberry Pi in order to create a SSH connection
"""
import paramiko
from scp import SCPClient

import os 
import time
import subprocess
import re

def createSSHClient(server, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=user, password=password)
    return client

hostname=subprocess.check_output(['hostname']).decode("utf-8") #Local hostname 
# print(hostname)

ips = subprocess.check_output(['arp', '-a']).decode("utf-8") 
#rExpression='\d+\.\d+\.\d+\.\d+\s+b8-27-eb-\w+-\w+-\w+'  #All Raspeberry pi 3 MAC Adress start with b8-27-eb
#rExpression='\d+\.\d+\.\d+\.\d+\s+dc-a6-32-\w+-\w+-\w+'  #All Raspeberry pi 4
rExpression='\d+\.\d+\.\d+\.\d+\s+(?:dc|b8)-(?:a6|27)-(?:32|eb)-\w+-\w+-\w+'  #All Raspeberry pi 3 and 4

raspberryConected= re.findall(rExpression, ips)

for raspberry in raspberryConected:
    ip=raspberry.split()[0]
    try:
        ssh = createSSHClient(ip, 'pi', 'raspberry') #change default user and pasword 
        scp = SCPClient(ssh.get_transport())
        scp.put("C:/Users/Alex/Desktop/YourFolder/yourFile.py", remote_path="/home/pi/Desktop/") #Change the paths as you required
        print("Archivo mandado correctamente a modulo con IP: " + ip) #File sent correctly to module with IP:
        # Prueba para reiniciar el modulo

        stdin, stdout, stderr = ssh.exec_command("python3 /home/pi/Desktop/yourFile.py") #You can changue the command as you required 

    except:
        print("Archivo no mandado a modulo con IP: " + ip) #File not sent to module with IP: 
    finally:
        ssh.close()

