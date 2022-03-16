class Machine:
    
    # instance attributes
    def __init__(self,id):
        self.id = id
        self.core = 1
        self.memory = 1
        self.core_used = 0
        self.memory_used = 0
        self.vm_dict = {}

    def addVM(self,vm):
        self.core_used +=  float(vm["core"])
        self.memory_used += float(vm["memory"])
        self.vm_dict[vm["vmId"]] = vm
    
    def removeVM(self,vm):
        self.core_used -=  float(vm["core"])
        self.memory_used -= float(vm["memory"])
        self.vm_dict.pop(vm["vmId"])

    def checkVm(self,vm):
        result = True
        if(self.core_used + float(vm["core"]) > 1):
            result = False
        elif (self.memory_used + float(vm["memory"]) > 1):
            result = False
        return result

    def remove_expired_vm(self,vmid):
        item = self.vm_dict[vmid]
        #print("vmId: " + item["vmId"] + " vmtype: " + item["vmTypeId"] + " was removed from machine " + str(self.id) + " core used: " + item["core"] + " memory used:" +item["memory"])
        self.removeVM(item)
        

    def __repr__(self) -> str:
         rep = 'machine( Core Used: ' +str(self.core_used) + ', Memory used: ' + str(self.memory_used) + ', number of vm inside machine: ' + str(len(self.vm_dict)) + ")"
         return rep

       
