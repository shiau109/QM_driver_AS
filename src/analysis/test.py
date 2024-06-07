import os, json

a_set_time = 7.2*60
folder_path = "/Users/ratiswu/Downloads/WS"
temp_folder_paths = [os.path.join(folder_path,name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path,name))]
for temperature_folder_path in temp_folder_paths:
    set_folders = [name for name in os.listdir(temperature_folder_path) if (os.path.isdir(os.path.join(temperature_folder_path,name)) and name[:8]=='Radiator')]
    time_past = []
    for i in range(len(set_folders)):
        time_past.append(float((i+1)*a_set_time))
    other_info = {}
    other_info["q3"] = {"start_time":"2024-05-14 18:15","refIQ":[0,0],"time_past":time_past,"f01":4.5e9}
    with open(os.path.join(temperature_folder_path,"otherInfo.json"),"w") as record_file:
        json.dump(other_info,record_file)