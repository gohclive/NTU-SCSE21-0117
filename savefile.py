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

def get_vm_request(con, starttime1, starttime2, limit):
    cur = con.cursor()
    cur.execute("select vm.vmId,vm.vmTypeId,priority,starttime,endtime, core, memory, machineId  from vm inner join vmType on vm.vmTypeId = vmType.vmTypeId where starttime > ? and starttime < ? and machineId = 16 order by CAST(starttime as float) limit ?",
                (starttime1, starttime2, limit))
    vm_request_list = cur.fetchall()
    print(vm_request_list[0])
    return vm_request_list


def get_vm_request_new(con,starttime1, starttime2):
    cur = con.cursor()
    query = "select vm.vmId,vm.vmTypeId,priority,starttime as \"time\", core, memory, machineId, 'start' as status from vm inner join vmType on vm.vmTypeId = vmType.vmTypeId where starttime >= ? and starttime <= ? and machineId = 16 and endtime is not null UNION select vm.vmId,vm.vmTypeId,priority,endtime as \"time\", core, memory, machineId, 'end' as status from vm inner join vmType on vm.vmTypeId = vmType.vmTypeId where starttime >= ? and starttime <= ? and machineId = 16 and time is not null order by time"
    cur.execute(query,(starttime1, starttime2, starttime1, starttime2))
    vm_request_list = cur.fetchall()
    return vm_request_list

# def get_vm_request_new(con,limit):
#     cur = con.cursor()
#     query = "select vm.vmId,vm.vmTypeId,priority,starttime as \"time\", core, memory, machineId, 'start' as status from vm inner join vmType on vm.vmTypeId = vmType.vmTypeId where starttime > 0 and starttime < 2 and machineId = 16 UNION select vm.vmId,vm.vmTypeId,priority,endtime as \"time\", core, memory, machineId, 'end' as status from vm inner join vmType on vm.vmTypeId = vmType.vmTypeId where starttime > 0 and starttime < 2 and machineId = 16 and time is not null order by time limit 2000"
#     cur.execute(query)
#     vm_request_list = cur.fetchall()
#     print(vm_request_list[0])
#     return vm_request_list

def get_vmType(con, vmId):
    cur = con.cursor()
    cur.execute(
        "select vmTypeId, core, memory from vmType where machineId = ? order by vmTypeId", (vmId,))
    rows = cur.fetchall()
    return rows

def save_to_csv(name,header,vmlist):
    with open(name,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(vmlist)

def save():
    """ This method creates the csv directory along with the relevent csv files used in this project."""

    con = create_connection()

    my_dir = Path("csv")
    if not my_dir.is_dir():
        print("csv folder not found, creating folder")
        my_dir.mkdir()
    if not (Path("csv/vm request list(0-2).csv").exists()):
        print("csv/vm request list(0-2).csv")
        vm_request_list = get_vm_request_new(con,0,2)
        header = ["vmId","vmTypeId","priority","time","core","memory", "machineId","status"]  
        save_to_csv("csv/vm request list(0-4).csv",header,vm_request_list)
    if not (Path("csv/vm request list(0-4).csv").exists()):
        print("vm request list(0-4) not found")
        vm_request_list = get_vm_request_new(con,0,4)
        header = ["vmId","vmTypeId","priority","time","core","memory", "machineId","status"]  
        save_to_csv("csv/vm request list(0-4).csv",header,vm_request_list)
    if not (Path("csv/vm request list(0-6).csv").exists()):
        print("vm request list(0-6) not found")
        vm_request_list = get_vm_request_new(con,0,6)
        header = ["vmId","vmTypeId","priority","time","core","memory", "machineId","status"]  
        save_to_csv("csv/vm request list(0-6).csv",header,vm_request_list)

    con.close()
    

if __name__ == '__main__':
    save()
