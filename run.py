import sys
import Algorithm as algo


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

for item in sys.argv:
    print(item)

if  "-h" in opts:
    print("Useage: run [VM_entry] [VM_type] [algo]")

if (len(sys.argv)!=4):
    print("usage run VM_Entry[csv] Vm_List[csv] [algo]")
else:
    print(sys.argv[1])
    vm_entry_list = algo.fileToDict(sys.argv[1])
    vm_list = algo.fileToDict(sys.argv[2])

    if (sys.argv[3] == "nextfit"):
        #next fit
        machine_list = algo.next_fit(vm_entry_list,vm_list)
        print("next fit")
        #print first 5 machine
        for i in range(5):
            print(machine_list[i])

        counter = 0
        for item in machine_list:
            counter += len(item.vm_list)

        print("number of physical machine required:"+str(len(machine_list)))
        print("----------------------------------------------------------------")
    elif (sys.argv[3] == "firstfit"):
        # first fit
        machine_list = algo.first_fit(vm_entry_list,vm_list)
        print("first fit")
        #print first 5 machine
        for i in range(5):
            print(machine_list[i])

        counter = 0
        for item in machine_list:
            counter += len(item.vm_list)

        print("number of physical machine required:"+str(len(machine_list)))
        print("----------------------------------------------------------------")
    elif (sys.argv[3] == "bestfit"):
        print("best fit algorithm")
        # best fit
        machine_list = algo.best_fit(vm_entry_list,vm_list)
        print("best fit")
        for i in range(5):
            print(machine_list[i])

        counter = 0
        for item in machine_list:
            counter += len(item.vm_list)
        print("number of VMs in physical machines:"+str(counter))
        print("number of physical machine required:"+str(len(machine_list)))
        print("----------------------------------------------------------------")
    elif (sys.argv[3] == "worsefit"):
        print("worst fit algorithm")
    else:
        print("invalid algorithm")
