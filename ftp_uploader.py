import ftplib
import os, fnmatch
      
def Diff(li1, li2): 
    return (list(set(li1) - (set(li2))))

def list_remote_files(ftp):
    ftp_list = []
    # Get the remote files
    data = []
    ftp.dir(data.append)
    pattern = "*.jpg"  
    for entry in data:  
        if fnmatch.fnmatch(entry, pattern):
                split_part = entry.split() #split to get only the name of the file
                ftp_list.append(split_part[-1]) #take the last element of the list (name of the file) and add it 
                
#     print("FTP jpg files list :")
#     print(ftp_list)
#     print("-----")    
    return ftp_list

def list_local_files(dir):       
    local_list = []
    # Get jpg local files
    listOfFiles = os.listdir(dir)  
    pattern = "*.jpg"  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
                local_list.append(entry)
    print("Local jpg files list :")
    print(local_list)
    print("-----")
    return local_list
    
# upload sequence
def upload_files(ftp, files_to_upload):
    for entry in files_to_upload:  
        print ("Uploading " + entry + "...") 
        ftp.storbinary('STOR ' + entry, entry)

#Delete uploaded files
def delete_files(local_list):
    for entry in local_list:  
        os.remove(entry)

