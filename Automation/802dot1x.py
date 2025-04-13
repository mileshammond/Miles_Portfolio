# By Miles Hammond

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
import csv
import re
import getpass
import pathlib

password = getpass.getpass(prompt="\nPlease enter you password: ")

IP_addresses=[]

with open('cisco_IP_list.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
   
    for row in data:  
       IP_addresses.append([row['IP Address'].strip(),row['Display Name'].strip()])

csvfile.close()

for IP in range(0,len(IP_addresses)):
    results=[]

    file_path = pathlib.Path(f"Non-Radius-{IP_addresses[IP][1]}.csv")

    if file_path.exists():
        continue
    else:
        device_dict = {
            "device_type" : "cisco_ios",
            "host" : IP_addresses[IP][0],
            "username": "mhammond",
            "password": password
        }

        try:
            cisco_switch=ConnectHandler(**device_dict)
            filter_hostname = cisco_switch.find_prompt()

            uptime=cisco_switch.send_command("show version | include uptime is")
            stack_size = cisco_switch.send_command(f"show switch detail",use_textfsm=True)
       
            results.append([f"{uptime}"])
            results.append([""])
            results.append(["Ports not configured for Radius 802.1x"])
            results.append([""])
            results.append(["Stack members ",len(stack_size)])

            interface_output = cisco_switch.send_command("show interfaces status",use_textfsm=True)

            for item in range(0,len(interface_output)):
               
                if(item==0):
                    print(f"\nChecking switch {filter_hostname[:-1]} on {IP_addresses[IP][0]}. {len(stack_size)} {'switch members' if len(stack_size)>1 else 'switch'}\n")
                    print(f"\nINTERFACE   VLAN    STATUS         MAC ADDRESS        NOTES\n")
                    results.append([""])
                    results.append(["","INTERFACE","VLAN","STATUS","MAC ADDRESS","NOTES"])

                usage=""

                if not interface_output[item]['port'].startswith(("Ap", "Po")):
                    radius_enabled_interfaces = cisco_switch.send_command(f"show dot1x interface {interface_output[item]['port']}",use_textfsm=True)

                    #If port doesnt have radius configured then continue to get port information
                    if len(radius_enabled_interfaces)==0:
                        MAC_address = cisco_switch.send_command(f"show mac address-table interface {interface_output[item]['port']}")

                        #Checking if current port has a device connected to it. No MAC adddress no device!  
                        MAC_search=re.search(r"\b[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\b",MAC_address)
                       
                        #Check if port has never been used since the switch has been UP
                        used_check = cisco_switch.send_command(f"show interfaces {interface_output[item]['port']} | include line protocol is | Last input never")

                        used=re.search("Last input never, output never, output hang never",used_check)

                        # Checking if device has MAC address
                        if not (MAC_search):
                            MAC_add="No MAC address"
                        else:
                            MAC_add=MAC_search.group().upper()

                        if(used):
                            usage="Never used since switch has been UP"

                        print(f"{interface_output[item]['port']}    {interface_output[item]['vlan_id']}     {interface_output[item]['status']}      {MAC_add}      {usage}")
                        results.append(["",interface_output[item]['port'],interface_output[item]['vlan_id'],interface_output[item]['status'],MAC_add,usage])
               
            with open(f"Non-Radius-{filter_hostname[:-1]}.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(results)

        # Handles Authentication error
        except NetmikoAuthenticationException:
            # Create file (if it doesnt already exist) for logging switch errors
            error_log=open(f"Switch_log_errors.txt", "a")
            error_log.write(f"Authentication failed on switch {IP_addresses[IP][0]}\n")
            print(f"\nAuthentication failed on switch {IP_addresses[IP][0]}")  
        # Handles timout error
        except NetmikoTimeoutException:
            # Create file (if it doesnt already exist) for logging switch errors
            error_log=open("Switch_log_errors.txt ","a")
            error_log.write(f"Session timeout on switch {IP_addresses[IP][0]}\n")
            print(f"\nSession timeout on switch {IP_addresses[IP][0]}")
