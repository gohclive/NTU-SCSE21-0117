class Machine:
    
    # instance attributes
    def __init__(self,id):
        self.id = id
        self.core = 1
        self.memory = 1
        self.core_used = 0
        self.memory_used = 0
        self.vm_list = []

    def addVM(self,vm):
        self.vm_list.append(vm)
        self.core_used +=  float(vm["core"])
        self.memory_used += float(vm["memory"])
    
    def removeVM(self,vm):
        self.vm_list.remove(vm)
        self.core_used -=  float(vm["core"])
        self.memory_used -= float(vm["memory"])

    def checkVm(self,vm):
        result = True
        if(self.core_used + float(vm["core"]) > 1):
            result = False
        elif (self.memory_used + float(vm["memory"]) > 1):
            result = False
        return result

    def __repr__(self) -> str:
         rep = 'machine( Core Used: ' +str(self.core_used) + ', Memory used: ' + str(self.memory_used) + ', number of vm inside machine: ' + str(len(self.vm_list)) + ")"
         return rep
