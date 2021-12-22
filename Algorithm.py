# libraries
import csv
from VM import *
from Machine import Machine
import savefile
import math


def fileToDict(filename):
    """ This method read the csv file and append them rows into a list """
    fileList = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # next(csv_reader) #skip headers
        for row in csv_reader:
            fileList.append(row)
    return fileList


def get_not_item(totalVms, vmList):
    # get vmId of vm not in machine 16
    total = []
    noOfVm = []
    for i in range(0, totalVms):
        total.append(i)

    for item in vmList:
        noOfVm.append(item.vmType)

    not_item = set(total) - set(noOfVm)
    return not_item


def find_VM_by_id(id, vm_type_list):
    for vm in vm_type_list:
        if(id == vm["vmTypeId"]):
            return True
    return False

def add_entry(dict, vmid, machineid):
    dict[vmid] = machineid

def remove_entry(dict, vmid):
    dict.pop(vmid)

def first_fit(vm_entry_list):
    """ This method uses first fit algorithm for bin packing
    vm machine entries are sorted by the start time and would be added to the physical machine.
    Parameters: (connection, list)
    Returns : a list of machines being used  """

    # get first 100 vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    # initiate and declare machine and list of machine
    machine_list = []
    m0 = Machine(0)
    machine_list.append(m0)

    #global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # loop through item in vm_list,
    # check if machine have available space, if True, add vm entry to machine
    # else create new machine instance, add vm to machine and append it to the list

    counter = 0
    print("x,y")
    for item in vm_list:
        if item["status"] == "start":
            for machine in machine_list:
                if(machine.checkVm(item)):
                    machine.addVM(item)
                    add_entry(vm_mach,item["vmId"],machine.id)
                    
                    break
            else:
                counter += 1
                m = Machine(counter)
                m.addVM(item)
                machine_list.append(m)
                add_entry(vm_mach,item["vmId"],m.id)
                
        else:
            machid = vm_mach[item["vmId"]]
            machine_list[machid].remove_expired_vm(item["vmId"])  
        machine_used_over_time(item["time"],len(machine_list))
    return machine_list


def next_fit(vm_entry_list):
    """This method check if current vm entry fits in current physical machine, if so place it in this machine, else start a new machine instance"""
    # get first 100 vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    #global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # initiate and declare machine and list of machine
    machine_list = []
    m0 = Machine(0)
    machine_list.append(m0)
    # loop through item in vm_list,
    # check if vm entry is in phyiscal machine 16, if invalid entry, break
    # check if machine have available space, if True, add vm entry to machine
    # else create new machine instance, add vm to machine and append it to the list

    counter = 0
    curr_mach = m0
    print("x,y")
    for item in vm_list:
        if item["status"] == "start":
            if(curr_mach.checkVm(item)):
                curr_mach.addVM(item)
                add_entry(vm_mach,item["vmId"],curr_mach.id)
            else:
                counter += 1
                m = Machine(counter)
                m.addVM(item)
                add_entry(vm_mach,item["vmId"],m.id)
                curr_mach = m
                machine_list.append(m)
        else:
            machid = vm_mach[item["vmId"]]
            machine_list[machid].remove_expired_vm(item["vmId"])
        machine_used_over_time(item["time"],len(machine_list))
    return machine_list


def best_fit(vm_entry_list):
    """This method checks for the machine with the tightest fit, if vm does not fit any machine, start a new machine instance and place vm in it """
    # get vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    #global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # find lower bound for vm entry core
    total_core = 0
    for item in vm_entry_list:
        total_core += float(item["core"])
    optimal_num_machine = math.ceil(total_core/1)

    # initalise and declare machine list and machine
    machine_list = []
    for i in range(optimal_num_machine):
        m = Machine(i)
        machine_list.append(m)

    print("x,y")
    for item in vm_list:
        vmcore = float(item["core"])
        closest_fit = 0
        chosen_machine = 0

        if item["status"] == "start":
            for m in machine_list:
                if(m.checkVm(item)):
                    if((vmcore+m.core_used) > closest_fit):
                        closest_fit = vmcore+m.core_used
                        chosen_machine = m
                else:
                    continue
            chosen_machine.addVM(item)
            add_entry(vm_mach,item["vmId"],chosen_machine.id)
        else:
            machid = vm_mach[item["vmId"]]
            machine_list[machid].remove_expired_vm(item["vmId"])
        machine_used_over_time(item["time"],len(machine_list))
    return machine_list


def worse_fit(vm_entry_list):
    # get vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    #global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # find lower bound for vm entry core
    total_core = 0
    for item in vm_entry_list:
        total_core += float(item["core"])
    optimal_num_machine = math.ceil(total_core/1)

    # initalise and declare machine list and machine
    machine_list = []
    for i in range(optimal_num_machine):
        m = Machine(i)
        machine_list.append(m)

    print("x,y")
    for item in vm_list:
        vmcore = float(item["core"])
        least_fit = 1
        chosen_machine = len(machine_list)+1

        if item["status"] == "start":
            for m in machine_list:
                if(m.checkVm(item)):
                    if((vmcore+m.core_used) < least_fit):
                        least_fit = vmcore+m.core_used
                        chosen_machine = m
                else:
                    # if none of the machine is available, create new machine instance
                    if(chosen_machine == len(machine_list)+1):
                        m = Machine(len(machine_list)+1)
                        chosen_machine = m
                        machine_list.append(m)
            chosen_machine.addVM(item)
            add_entry(vm_mach,item["vmId"],chosen_machine.id)
        else:
            machid = vm_mach[item["vmId"]]
            machine_list[machid].remove_expired_vm(item["vmId"])
        machine_used_over_time(item["time"],len(machine_list))
    return machine_list


def machine_used_over_time(time,no_of_machine):
    print(time,no_of_machine,sep=",")

def main():
    # get relevant files and store them in a dictionary
    vm_type_list = fileToDict("csv/vm type list.csv")
    vm_entry = fileToDict("csv/vm entry list.csv")

    # get total number of vmTypes that is in machine 16 and store them in list

    print("total number of vm types: " + str(len(vm_type_list)))
    print("----------------------------------------------------------------")

    # offline algorithm

    # next fit
    machine_list = next_fit(vm_entry)
    print("next fit")
    # print first 5 machine
    for i in range(5):
        print(machine_list[i])

    counter = 0
    for item in machine_list:
        counter += len(item.vm_list)
    print("number of VMs in physical machines:"+str(counter))
    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")

    # first fit
    machine_list = first_fit(vm_entry)
    print("first fit")
    # print first 5 machine
    for i in range(5):
        print(machine_list[i])

    counter = 0
    for item in machine_list:
        counter += len(item.vm_list)
    print("number of VMs in physical machines:"+str(counter))
    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")

    # best fit
    machine_list = best_fit(vm_entry)
    print("best fit")
    for i in range(5):
        print(machine_list[i])

    counter = 0
    for item in machine_list:
        counter += len(item.vm_list)
    print("number of VMs in physical machines:"+str(counter))
    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")

    # Worse fit
    machine_list = worse_fit(vm_entry)
    print("worse fit")

    counter = 0
    for item in machine_list:
        print(item)
        counter += len(item.vm_list)

    print("number of VMs in physical machines:"+str(counter))
    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")


def test():
    # get relevant files and store them in a dictionary
    vm_type_list = fileToDict("csv/vm type list.csv")
    vm_entry = fileToDict("csv/vm entry list.csv")

    # next fit
    # machine_list = first_fit(vm_entry)

    # next fit
    #machine_list = next_fit(vm_entry)

    # best fit
    machine_list = best_fit(vm_entry)

    # worst fit
    #machine_list = next_fit(vm_entry)

if __name__ == '__main__':
    savefile.save()
    test()
