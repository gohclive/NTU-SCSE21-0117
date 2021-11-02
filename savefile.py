import sqlite3
from sqlite3 import Error
import csv
from pathlib import Path

VM_ID = 16

def create_connection():
    # Create a SQL connection to our SQLite database
    con = None
    db = "packing_trace_zone_a_v1.sqlite"
    try:
        con = sqlite3.connect(db)
    except Error as e:
        print(e)
    return con

def get_vm_entry(con, starttime1, starttime2, limit):
    cur = con.cursor()
    cur.execute("select vm.vmId,vm.vmTypeId,priority,starttime,endtime, core, memory, machineId  from vm inner join vmType on vm.vmTypeId = vmType.vmTypeId where starttime > ? and starttime < ? and machineId = 16 order by CAST(starttime as float) limit ?",
                (starttime1, starttime2, limit))
    vm_entry_list = cur.fetchall()
    print(vm_entry_list[0])
    return vm_entry_list

def get_vmType(con, vmId):
    cur = con.cursor()
    cur.execute(
        "select vmTypeId, core, memory from vmType where machineId = ? order by vmTypeId", (vmId,))
    rows = cur.fetchall()
    return rows

def save_to_csv(name,header,l):
    with open(name,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(l)

def save():
    """ This method creates the csv directory along with the relevent csv files used in this project."""

    con = create_connection()

    my_dir = Path("csv")
    if not my_dir.is_dir():
        print("csv folder not found, creating folder")
        my_dir.mkdir()
    
    if  not (Path("csv/vm type list.csv").exists()):
        print("vm type list not found, creating vm type list.csv")
        vm_type_list = get_vmType(con,VM_ID)
        header = ["vmTypeId","core","memory"]
        save_to_csv("csv/vm type list.csv",header,vm_type_list)
    if not (Path("csv/vm entry list.csv").exists()):
        print("vm entry list entry not found, creating vm entry list.csv")
        vm_entry_list = get_vm_entry(con,0,2,"5204184")
        header = ["vmId","vmTypeId","priority","starttime","endtime","core","memory", "machineId"]  
        save_to_csv("csv/vm entry list.csv",header,vm_entry_list)
    if not (Path("csv/vm entry list(1000).csv").exists()):
        print("vm entry list(1000) not found")
        vm_entry_list = get_vm_entry(con,0,2,1000)
        header = ["vmId","vmTypeId","priority","starttime","endtime","core","memory", "machineId"]  
        save_to_csv("csv/vm entry list(1000).csv",header,vm_entry_list)
    if not (Path("csv/vm entry list(100).csv").exists()):
        print("vm entry list(100) not found")
        vm_entry_list = get_vm_entry(con,0,2,100)
        header = ["vmId","vmTypeId","priority","starttime","endtime","core","memory", "machineId"]  
        save_to_csv("csv/vm entry list(100).csv",header,vm_entry_list)
    con.close()


if __name__ == '__main__':
    save()
