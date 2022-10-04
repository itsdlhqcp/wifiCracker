import subprocess
import re


cmd_ouput = subprocess.run(['netsh','wlan','show','profiles'],
capture_output=True).stdout.decode()

wifi_list=[]

profile_names = re.findall("All User Profile      :(.*)\r",cmd_ouput)


if profile_names != 0:
    for name in profile_names:
        wifi_profile={} #to store wifi data
        profile_info = subprocess.run(['netsh','wlan','show','profiles',name],capture_output=True).stdout.decode()

        if re.search("Security key        :Absent",profile_info):
            continue
        else:
            wifi_profile['ssid']  = name
            profile_info_password = subprocess.run(['netsh','wlan','show','profiles',name,'key=clear'],capture_output=True).stdout.decode()
            password = re.search("Key Content         :(.*)\r",profile_info_password)  
            if password == None:
                wifi_profile['password']=None
            else:
                wifi_profile['password']=password[1]
        wifi_list.append(wifi_profile)

for i in range(len(wifi_list)):
    print(wifi_list[i])
