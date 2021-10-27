class VM:
     # instance attributes
    def __init__(self,type,core,memory):
        self.vmType = type
        self.core = core
        self.memory = memory
    
    def __repr__(self) -> str:
         rep = 'VM(' +str(self.vmType) + ',' + str(self.core) + ',' + str(self.memory) + ")"
         return rep

class Entry:
     # instance attributes
    def __init__(self,vmTypeId,priority,starttime,endtime):
        self.vmTypeId = vmTypeId
        self.priority = priority
        self.starttime = starttime
        self.endtime = endtime
    
    def __repr__(self) -> str:
         rep = 'Entry(' +str(self.vmTypeId) + ',' + str(self.priority) + ',' + str(self.starttime) + ',' + str(self.endtime) + ")"
         return rep

    
