import sys
import Algorithm as algo
import savefile


def print_algo(method, vm_request_list):
    maxmachine = method(vm_request_list)
    print(maxmachine)


def main():
    if (len(sys.argv) != 4):
        print("Usage:\n1.run.py VM_request[csv] Vm_List[csv] [algo]")
        print("2.run.py VM_request[csv] Vm_List[csv] -a")
    else:
        vm_request_list = algo.fileToDict(sys.argv[1])
        vm_list = algo.fileToDict(sys.argv[2])
        if (sys.argv[3] == "-a"):
            # next fit
            print("next fit")
            print_algo(algo.next_fit, vm_request_list)

            # first fit
            print("first fit")
            print_algo(algo.first_fit, vm_request_list)

            # best fit
            print("best fit")
            print_algo(algo.best_fit, vm_request_list)

            # worst fit
            print("worst fit")
            print_algo(algo.worse_fit, vm_request_list)

        elif (sys.argv[3] == "nextfit"):
            # next fit
            print("next fit")
            print_algo(algo.next_fit, vm_request_list)

        elif (sys.argv[3] == "firstfit"):
            # first fit
            print("first fit")
            print_algo(algo.next_fit, vm_request_list)

        elif (sys.argv[3] == "bestfit"):
            # best fit
            print("best fit")
            print_algo(algo.best_fit, vm_request_list)

        elif (sys.argv[3] == "worsefit"):
            # Worse fit
            print("worst fit")
            print_algo(algo.worse_fit, vm_request_list)

        else:
            print("invalid algorithm")


if __name__ == '__main__':
    savefile.save()
    main()
