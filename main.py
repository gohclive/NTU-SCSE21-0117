# libraries
import csv
from VM import *
from Machine import Machine
import savefile

def fileToDict(filename):
    """ This method read the csv file and append them rows into a list """
    fileList = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        next(csv_reader) #skip headers
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
            return vm


def first_fit(vm_entry_list,vm_type_list):
    """ This method uses first come first serve algorithm for bin packing
    vm machine entries are sorted by the start time and would be added to the physical machine.
    This algorithm did not account for the endtime of the vm entry.
    Parameters: (connection, list)
    Returns : a list of machines being used  """

    # get first 100 vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    # initiate and declare machine and list of machine
    machine_list = []
    m0 = Machine()
    machine_list.append(m0)
    # loop through item in vm_list,
    # check if vm entry is in phyiscal machine 16, if invalid entry, break
    # check if machine have available space, if True, add vm entry to machine
    # else create new machine instance, add vm to machine and append it to the list

    counter = 0
    for item in vm_list:
        for machine in machine_list:
            vm = find_VM_by_id(item["vmTypeId"], vm_type_list)
            if (vm == None):
                break
            if(machine.checkVm(vm)):
                machine.addVM(vm)
                break
        else:
            m = Machine()
            m.addVM(vm)
            machine_list.append(m)    
    return machine_list


def Fit(vm_entry_list,vm_type_list,mode):
    # get first 100 vm entries where start time is between 0 and 2 arrange by core
    vm_list = vm_entry_list
    sorted_list = []
    if (mode == "best"):
        sorted_list = sorted(vm_list,key=lambda d: d["core"],reverse=True)
    elif(mode == "worst"):
        sorted_list = sorted(vm_list,key=lambda d: d["core"])

    # initiate and declare machine and list of machine
    machine_list = []
    m0 = Machine()
    machine_list.append(m0)
    # loop through item in vm_list,
    # check if vm entry is in phyiscal machine 16, if invalid entry, break
    # check if machine have available space, if True, add vm entry to machine
    # else create new machine instance, add vm to machine and append it to the list

    counter = 0
    for item in sorted_list:
        for machine in machine_list:
            vm = find_VM_by_id(item["vmTypeId"], vm_type_list)
            if (vm == None):
                break
            if(machine.checkVm(vm)): 
                machine.addVM(vm)
                break
        else:
            m = Machine()
            m.addVM(vm)
            machine_list.append(m)
    return machine_list


def main():

    # get total number of vmTypes that is in machine 16 and store them in list
    vm_type_list = fileToDict("csv/vm type list.csv")
    print("total number of vm types: " + str(len(vm_type_list)))
    print("----------------------------------------------------------------")


    # online algorithm
    # first fit
    vm_entry_1000 = fileToDict("csv/vm entry list(1000).csv")
    machine_list = first_fit(vm_entry_1000,vm_type_list)
    
    #print first 5 machine
    for i in range(5):
        print(machine_list[i])

    counter = 0
    for item in machine_list:
        counter += len(item.vm_list)

    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")

    # best fit
    machine_list = Fit(vm_entry_1000,vm_type_list,"best")

     #print first 5 machine
    for i in range(5):
        print(machine_list[i])

    counter = 0
    for item in machine_list:
        counter += len(item.vm_list)
    print("number of VMs in physical machines:"+str(counter))
    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")

    # Worse fit
    machine_list = Fit(vm_entry_1000,vm_type_list,"worst")

     #print first 5 machine
    for i in range(5):
        print(machine_list[i])

    counter = 0
    for item in machine_list:
        counter += len(item.vm_list)

    print("number of VMs in physical machines:"+str(counter))
    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")

if __name__ == '__main__':
    savefile.save()
    main()
