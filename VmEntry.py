class VMEntry:
     # instance attributes
    def __init__(self,vmTypeId,priority,starttime,endtime):
        self.vmTypeId = vmTypeId
        self.priority = priority
        self.starttime = starttime
        self.endtime = endtime
    
    def __repr__(self) -> str:
         rep = 'VM(' +str(self.vmType) + ',' + str(self.core) + ',' + str(self.memory) + ")"
         return rep
