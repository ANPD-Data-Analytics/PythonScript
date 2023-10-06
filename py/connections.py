import os

sysUser511 =os.getlogin()
#print (sysUser511)
#print (os.getcwd() )
os.chdir("C:/Users/"+sysUser511+"/OneDrive - Abbott/LoginInfo")
wd = os.getcwd() 
try:
    with open("CDP_Connection_String.txt", "r") as file:
        cdp_con = file.read()
        #print(cdp_con)
except FileNotFoundError:
    cdp_con = None

try:
    with open("Shiloh_acc_key.txt", "r") as file:
        shi_key = file.read()
        #print(shi_key)
except FileNotFoundError:
    shi_key = None

try:
    with open("Shiloh_acc_name.txt", "r") as file:
        shi_name = file.read()
        #print(shi_name)
except FileNotFoundError:
    shi_name = None
os.makedirs("C:/Users/"+sysUser511+"/Documents/Python Scripts11/log",exist_ok=True)
os.chdir("C:/Users/"+sysUser511+"/Documents/Python Scripts")

