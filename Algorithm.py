# libraries
import csv
from VM import *
from Machine import Machine
import savefile
import time


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

    start_time = time.time()
    f = open("output/firstfit.txt", 'w')

    # get first 100 vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    # initiate and declare machine and list of machine
    machine_list = []
    m0 = Machine(0)
    machine_list.append(m0)

    # global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # counters
    maxmachine = 0

    # loop through item in vm_list,
    # check if machine have available space, if True, add vm entry to machine
    # else create new machine instance, add vm to machine and append it to the list

    # count the number of physical machine use
    machine_counter = 0

    machid = 0
    f.write("x,y\n")
    for item in vm_list:
        if item["status"] == "start":
            for machine in machine_list:
                if(machine.checkVm(item)):
                    if len(machine.vm_dict) == 0:
                        machine_counter += 1
                    machine.addVM(item)
                    add_entry(vm_mach, item["vmId"], machine.id)
                    break
            else:
                machid += 1
                m = Machine(machid)
                m.addVM(item)
                machine_list.append(m)
                machine_counter += 1
                add_entry(vm_mach, item["vmId"], m.id)
        else:
            id = vm_mach[item["vmId"]]
            for m in machine_list:
                if m.id == id:
                    if (len(m.vm_dict) == 1):
                        machine_counter -= 1
                        machine_list.remove(m)
                    else:
                        m.remove_expired_vm(item["vmId"])
                    break
            remove_entry(vm_mach, item["vmId"])
        output = str(item["time"]) + "," + str(machine_counter)+"\n"
        f.write(output)
        if machine_counter > maxmachine:
            maxmachine = machine_counter

    f.close()
    for machine in machine_list:
        if len(machine.vm_dict) != 0:
            machine_running += 1
            vm_running += len(machine.vm_dict)
    with open("analysis.txt", "a") as a:
        a.write("First Fit Analysis\n")
        a.write("max machine used: " + str(maxmachine))
        a.write("\n")
        a.write(str(time.time() - start_time))
        a.write("\n")
        a.write("----------------------------------------------------------------\n")
    return machine_list


def next_fit(vm_entry_list):
    """This method check if current vm entry fits in current physical machine, if so place it in this machine, else start a new machine instance"""

    start_time = time.time()
    f = open("output/nextfit.txt", 'w')

    # get first 100 vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    # global dictionary to link vm and physical machine
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

    # counter
    machine_counter = 0
    maxmachine = 0

    machid = 0
    curr_mach = m0
    f.write("x,y\n")
    for item in vm_list:
        if item["status"] == "start":
            if(curr_mach.checkVm(item)):
                if len(curr_mach.vm_dict) == 0:
                    machine_counter += 1
                curr_mach.addVM(item)
                add_entry(vm_mach, item["vmId"], curr_mach.id)
            else:
                machid += 1
                m = Machine(machid)
                m.addVM(item)
                add_entry(vm_mach, item["vmId"], m.id)
                machine_counter += 1
                curr_mach = m
                machine_list.append(m)
        else:
            id = vm_mach[item["vmId"]]
            machine_list[id].remove_expired_vm(item["vmId"])
            if len(machine_list[id].vm_dict) == 0:
                machine_counter -= 1
            remove_entry(vm_mach, item["vmId"])
        output = str(item["time"]) + "," + str(machine_counter)+"\n"
        f.write(output)
        if machine_counter > maxmachine:
            maxmachine = machine_counter

    f.close()
    with open("analysis.txt", "a") as a:
        a.write("next Fit Analysis\n")
        a.write("max machine used: " + str(maxmachine))
        a.write("\n")
        a.write(str(time.time() - start_time))
        a.write("\n")
        a.write("----------------------------------------------------------------\n")

    return machine_list


def best_fit(vm_entry_list):
    """This method checks for the machine with the tightest fit, if vm does not fit any machine, start a new machine instance and place vm in it """
    start_time = time.time()
    f = open("output/bestfit.txt", "w")
    # get vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    # global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # initalise and declare machine list and add 1 machine to list
    machine_list = []
    machid = 0
    m = Machine(machid)
    machine_list.append(m)

    # counter
    maxmachine = 0
    machine_counter = 0

    f.write("x,y\n")
    for item in vm_list:
        vmcore = float(item["core"])
        vmmem = float(item["memory"])
        # check vm status, add vm to chosen machine if status = start, remove vm if status = end
        if item["status"] == "start":
            chosen_machine = None
            # find optimal machine by sorting the machine list
            machine_list.sort(
                reverse=True, key=lambda i: i.memory_used+i.core_used)
            for m in machine_list:
                if vmcore+m.core_used <= m.core and vmmem+m.memory_used <= m.memory:
                    chosen_machine = m
                    break
            if chosen_machine == None:
                machid += 1
                m = Machine(machid)
                machine_list.append(m)
                chosen_machine = m

            if len(chosen_machine.vm_dict) == 0:
                machine_counter += 1
            chosen_machine.addVM(item)
            add_entry(vm_mach, item["vmId"], chosen_machine.id)
        else:
            id = vm_mach[item["vmId"]]
            # list is sorted, find index of machine where machine.id = id
            for m in machine_list:
                if m.id == id:
                    if len(m.vm_dict) == 1:
                        machine_counter -= 1
                        machine_list.remove(m)
                    else:
                        m.remove_expired_vm(item["vmId"])
                    break
            remove_entry(vm_mach, item["vmId"])

        output = str(item["time"]) + "," + str(machine_counter)+"\n"
        f.write(output)
        if machine_counter > maxmachine:
            maxmachine = machine_counter
    f.close()
    with open("analysis.txt", "a") as a:
        a.write("best Fit Analysis\n")
        a.write("max machine used: " + str(maxmachine))
        a.write("\n")
        a.write(str(time.time() - start_time))
        a.write("\n")
        a.write("----------------------------------------------------------------\n")
    return machine_list


def best_fit_by_resource(vm_entry_list, resource):
    """This method checks for the machine with the tightest fit, if vm does not fit any machine, start a new machine instance and place vm in it 
        resource : core/memory
    """

    start_time = time.time()
    f = open("output/bestfit("+resource+").txt", "w")
    # get vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    # global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # initalise and declare machine list and add 1 machine to list
    machine_list = []
    machid = 0
    m = Machine(machid)
    machine_list.append(m)

    # counters
    machine_counter = 0
    maxmachine = 0

    f.write("x,y\n")
    for item in vm_list:
        vmcore = float(item["core"])
        vmmem = float(item["memory"])

        # check vm status, add vm to chosen machine if status = start, remove vm if status = end
        if item["status"] == "start":
            chosen_machine = None
            # find optimal machine by sorting the machine list
            if(resource == "core"):
                machine_list.sort(reverse=True, key=lambda i: i.core_used)
            else:
                machine_list.sort(reverse=True, key=lambda i: i.memory_used)

            for m in machine_list:
                if vmcore+m.core_used <= m.core and vmmem+m.memory_used <= m.memory:
                    chosen_machine = m
                    break
            if chosen_machine == None:
                machid += 1
                m = Machine(machid)
                machine_list.append(m)
                chosen_machine = m

            if len(chosen_machine.vm_dict) == 0:
                machine_counter += 1
            chosen_machine.addVM(item)
            add_entry(vm_mach, item["vmId"], chosen_machine.id)

        else:
            id = vm_mach[item["vmId"]]
            # list is sorted, find index of machine where machine.id = id
            for m in machine_list:
                if m.id == id:
                    if len(m.vm_dict) == 1:
                        machine_counter -= 1
                        machine_list.remove(m)
                    else:
                        m.remove_expired_vm(item["vmId"])
                    break
            remove_entry(vm_mach, item["vmId"])
        output = str(item["time"]) + "," + str(machine_counter)+"\n"
        f.write(output)
        if machine_counter > maxmachine:
            maxmachine = machine_counter
    f.close()
    with open("analysis.txt", "a") as a:
        a.write("best Fit "+resource+" Analysis\n")
        a.write("max machine used: " + str(maxmachine))
        a.write("\n")
        a.write(str(time.time() - start_time))
        a.write("\n")
        a.write("----------------------------------------------------------------\n")
    return machine_list


def worse_fit(vm_entry_list):

    start_time = time.time()
    f = open("output/worsefit.txt", "w")

    # get vm entries where start time is between 0 and 2
    vm_list = vm_entry_list

    # global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # initalise and declare machine list and add 1 machine to list
    machine_list = []
    machid = 0
    m = Machine(machid)
    machine_list.append(m)

    machine_counter = 0
    maxmachine = 0

    f.write("x,y\n")
    for item in vm_list:
        vmcore = float(item["core"])
        vmmem = float(item["memory"])

        # check vm status, add vm to chosen machine if status = start, remove vm if status = end
        if item["status"] == "start":
            chosen_machine = None
            # find optimal machine by sorting the machine
            machine_list.sort(key=lambda i: i.core_used+i.memory_used)
            for m in machine_list:
                if m.core_used+vmcore <= m.core and m.memory_used+vmmem <= m.memory:
                    chosen_machine = m
                    break
            if chosen_machine == None:
                machid += 1
                m = Machine(machid)
                machine_list.append(m)
                chosen_machine = m

            if len(chosen_machine.vm_dict) == 0:
                machine_counter += 1
            chosen_machine.addVM(item)
            add_entry(vm_mach, item["vmId"], chosen_machine.id)

        else:
            id = vm_mach[item["vmId"]]
            # list is sorted, find index of machine where machine.id = id
            for m in machine_list:
                if m.id == id:
                    if len(m.vm_dict) == 1:
                        machine_counter -= 1
                        machine_list.remove(m)
                    else:
                        m.remove_expired_vm(item["vmId"])
                    break
            remove_entry(vm_mach, item["vmId"])
        output = str(item["time"]) + "," + str(machine_counter)+"\n"
        f.write(output)
        if machine_counter > maxmachine:
            maxmachine = machine_counter
    f.close()
    with open("analysis.txt", "a") as a:
        a.write("Worse Fit Analysis\n")
        a.write("max machine used: " + str(maxmachine))
        a.write("\n")
        a.write(str(time.time() - start_time))
        a.write("\n")
        a.write("----------------------------------------------------------------\n")
    return machine_list


def worse_fit_by_resource(vm_entry_list, resource):
    # get vm entries where start time is between 0 and 2
    start_time = time.time()
    f = open("output/worseFit("+resource+").txt", "w")
    vm_list = vm_entry_list

    # global dictionary to link vm and physical machine
    #key = vmId, value = machine
    vm_mach = {}

    # initalise and declare machine list and add 1 machine to list
    machine_list = []
    machid = 0
    m = Machine(machid)
    machine_list.append(m)

    machine_counter = 0
    maxmachine = 0

    f.write("x,y\n")
    for item in vm_list:
        vmcore = float(item["core"])
        vmmem = float(item["memory"])

        # check vm status, add vm to chosen machine if status = start, remove vm if status = end
        if item["status"] == "start":
            chosen_machine = None
            # find optimal machine by sorting the machine
            if(resource == "core"):
                machine_list.sort(key=lambda i: i.core_used)
            else:
                machine_list.sort(key=lambda i: i.memory_used)
            for m in machine_list:
                if m.core_used+vmcore <= m.core and m.memory_used+vmmem <= m.memory:
                    chosen_machine = m
                    break
            if chosen_machine == None:
                machid += 1
                m = Machine(machid)
                machine_list.append(m)
                chosen_machine = m
            if len(chosen_machine.vm_dict) == 0:
                machine_counter += 1
            chosen_machine.addVM(item)
            add_entry(vm_mach, item["vmId"], chosen_machine.id)

        else:
            id = vm_mach[item["vmId"]]
            for m in machine_list:
                if m.id == id:
                    if len(m.vm_dict) == 1:
                        machine_counter -= 1
                        machine_list.remove(m)
                    else:
                        m.remove_expired_vm(item["vmId"])
                    break
            remove_entry(vm_mach, item["vmId"])
        output = str(item["time"]) + "," + str(machine_counter)+"\n"
        f.write(output)
        if machine_counter > maxmachine:
            maxmachine = machine_counter
    f.close()
    with open("analysis.txt", "a") as a:
        a.write("Worse Fit "+resource+" Analysis\n")
        a.write("max machine used: " + str(maxmachine))
        a.write("\n")
        a.write(str(time.time() - start_time))
        a.write("\n")
        a.write("----------------------------------------------------------------\n")
    return machine_list


def machine_used_over_time(time, machine_list):
    count = 0
    for machine in machine_list:
        if(len(machine.vm_dict) != 0):
            count += 1
    print(time, count, sep=",")


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
    #vm_entry_02 = fileToDict("csv/vm entry list(0-2).csv")
    vm_entry_04 = fileToDict("csv/vm entry list(0-4).csv")
    #vm_entry_06 = fileToDict("csv/vm entry list(0-6).csv")
    #vm_entry_short = fileToDict("csv/vm entry list(4000).csv")

    # first fit
    #machine_list = first_fit(vm_entry_02)

    # next fit
    #machine_list = next_fit(vm_entry_02)

    # best fit
    #machine_list = best_fit(vm_entry_02)

    # best fit by resource
    machine_list = best_fit_by_resource(vm_entry_04, "core")
    machine_list = best_fit_by_resource(vm_entry_04, "memory")

    # worst fit
    #machine_list = worse_fit(vm_entry_06)
    machine_list = worse_fit_by_resource(vm_entry_04, "core")
    machine_list = worse_fit_by_resource(vm_entry_04, "memory")


if __name__ == '__main__':
    # savefile.save()
    start_time = time.time()
    print(str(start_time))
    test()
    print(str(time.time() - start_time))
