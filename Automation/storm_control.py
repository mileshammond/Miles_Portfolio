# Update switch estate with storm control commands.

# Please create files:  
# 1. IP.csv = List of switch stack IPs
# 2. commands.txt = List of commands for updating to a switch

# Automatically creates a text file with the devices configuration updates called "Storm Control Updates- <today date and time>.txt"
# Automatically creates a text file of the original AP port configuration called "Port Config Backup- <today date and time>.txt"

# Created by Miles Hammond.

from netmiko import *
import getpass
from datetime import *
import csv

# Create progress file for updating devices
date_stamp = datetime.now()
file_name=date_stamp.strftime("%A %d %B %Y %H.%M %p")+".txt"
results=open(f"C:\\Users\miles\OneDrive\Desktop\Python\Progs\Miles\Automation\Storm-Updates-{file_name}", "a")

# Create list of commands for updating configuration
commands_f = open("DATA_FILES/commands.txt", "r")
batch_commands=[]

for commands_line in commands_f:
   batch_commands.append(commands_line.strip())
commands_f.close  

original_no_of_batch_commands=len(batch_commands)

if(original_no_of_batch_commands==0):
   print("\nNo commands provided! Please provide commands to update port configuration!\n")
   results.write("\nNo commands provided! Please provided commands to update port configuration!")
else:
   # Enter switch credentials
   username = str(input("\nPlease enter username: "))
   password = getpass.getpass(prompt="\nPlease enter you password: ")

   # Create list of switch stack IP addresses
   IP_addresses=[]

   with open('DATA_FILES/IP.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
   
    for row in data:   
       IP_addresses.append(row['ip'])
    
   # Number of IP addresses in list
   no_of_IP_addresses=len(IP_addresses)

   # Check each switch in the global estate
   for IP in range(no_of_IP_addresses): 
       # Data stucture for connecting to CISCO switch stack 
       device_dict = {
           "device_type" : "cisco_ios",
           "host" : IP_addresses[IP],
           "username": username,
           "password": password
       }
       
       try:
           CISCO_switch = ConnectHandler(**device_dict)

           # Find hostname of current switch stack
           filter_hostname = CISCO_switch.find_prompt()

           print(f"\nChecking switch {IP_addresses[IP]} ({filter_hostname[:-1]}\n")

           # Create file (if it doesnt already exist) for backing up switch port config   
           file_name=date_stamp.strftime("%A %d %B %Y %H.%M %p")+".txt"
           backup=open(f"C:\\Users\miles\OneDrive\Desktop\Python\Progs\Miles\Automation\Port_Config_Backup-{file_name}", "a")

           backup_port_config=CISCO_switch.send_command("show config",read_timeout=120)
           backup.write(f"\n\n*** Switch {IP_addresses[IP]} ({filter_hostname[:-1]}) ***")
           backup.write(f"\n\n{backup_port_config}")
           backup.close

           # Using TextFSM to retrieve structured data
           output = CISCO_switch.send_command("show interfaces status",use_textfsm=True,read_timeout=120)

           Interface_rows=len(output)

           for row in range(0,Interface_rows):
               port = [row]['port']
               vlan = [row]['vlan_id']

               # VLANS: 160 is Wired. 170 is Corp sensor. 175 is AV. 190 is Security
               if(vlan == "160" or vlan == "170" or vlan == "175" or vlan == "190"):
                   # Position the current port interface into the command config
                   current_no_of_batch_commands=len(batch_commands)

                   if(current_no_of_batch_commands==original_no_of_batch_commands):     
                       batch_commands.insert(1, f'interface {port}')
                   else:  
                       batch_commands[1]=f'interface {port}'

                   # Update port configuration of current interface
                   CISCO_switch.send_config_set(batch_commands,read_timeout=120)
                   print(f"Adding storm control to port {port} in VLAN {vlan}\n")
                   adjusted_config=CISCO_switch.send_command(f"show run interface {port} | section interface",read_timeout=120)
                   results.write(f"\n\n {IP_addresses[IP]} ({filter_hostname[:-1]})")
                   results.write(f"\n\n {adjusted_config}")

           CISCO_switch.send_command("wr mem",read_timeout=120)       

       # Handles Authentication error
       except NetmikoAuthenticationException:
           print(f"\nAuthentication failed on switch {IP_addresses[IP]}") 
           results.write(f"\nAuthentication failed on switch {IP_addresses[IP]}\n")
          
       # Handles timout error 
       except NetmikoTimeoutException:
           print(f"\nSession timeout on switch {IP_addresses[IP]}") 
           results.write(f"\nSession timeout on switch {IP_addresses[IP]}\n") 
             
   # Finished updating switch estate!
   results.close

   print("\nFinished!\n") 

