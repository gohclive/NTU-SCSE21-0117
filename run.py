import sys
import Algorithm as algo


def print_algo(method, vm_entry_list, vm_list,option):
    machine_list = method(vm_entry_list, vm_list,option)
    for item in machine_list:
        print(item)
        item.get_vm_list()
        print("----------------------------------------------------------------")

    counter = 0
    for item in machine_list:
        counter += len(item.vm_list)

    print("number of physical machine required:"+str(len(machine_list)))
    print("----------------------------------------------------------------")


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if "-h" in opts:
    print("Useage: run [VM_entry] [VM_type] [algo]")


if (len(sys.argv) != 4):
    print("usage run VM_Entry[csv] Vm_List[csv] [algo]")
else:
    vm_entry_list = algo.fileToDict(sys.argv[1])
    vm_list = algo.fileToDict(sys.argv[2])

    if (sys.argv[3] == "-a"):
        # next fit
        print("next fit")
        print_algo(algo.next_fit, vm_entry_list, vm_list,"")
        # next fit with remove vm option
        print("next fit with remove vm option")
        print_algo(algo.next_fit, vm_entry_list, vm_list,"r")

        # first fit
        print("first fit")
        print_algo(algo.first_fit, vm_entry_list, vm_list,"")
        # first fit with remove vm option
        print("next fit with remove vm option")
        print_algo(algo.first_fit, vm_entry_list, vm_list,"r")

        # best fit
        print("best fit")
        print_algo(algo.best_fit, vm_entry_list, vm_list,"")
        # best fit with remove vm option
        print("best fit with remove vm option")
        print_algo(algo.best_fit, vm_entry_list, vm_list,"r")

        # worst fit
        print("worst fit")
        print_algo(algo.worse_fit, vm_entry_list, vm_list,"")
        # worst fit with remove vm option
        print("worst fit with remove vm option")
        print_algo(algo.worse_fit, vm_entry_list, vm_list,"r")

    elif (sys.argv[3] == "nextfit"):
        # next fit
        print("next fit")
        if "-r" in opts:
            print_algo(algo.next_fit, vm_entry_list, vm_list,"r")
        else:
            print_algo(algo.next_fit, vm_entry_list, vm_list,"")
    elif (sys.argv[3] == "firstfit"):
        # first fit
        print("first fit")
        if "-r" in opts:
            print_algo(algo.next_fit, vm_entry_list, vm_list,"r")
        else:
            print_algo(algo.next_fit, vm_entry_list, vm_list,"")
    elif (sys.argv[3] == "bestfit"):
        # best fit
        print("best fit")
        if "-r" in opts:
            print_algo(algo.best_fit, vm_entry_list, vm_list,"r")
        else:
            print_algo(algo.best_fit, vm_entry_list, vm_list,"")
    elif (sys.argv[3] == "worsefit"):
        # Worse fit
        print("worst fit")
        if "-r" in opts:
            print_algo(algo.worse_fit, vm_entry_list, vm_list,"r")
        else:
            print_algo(algo.worse_fit, vm_entry_list, vm_list,"")
    else:
        print("invalid algorithm")
