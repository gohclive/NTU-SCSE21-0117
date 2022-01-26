class VMRequest:
     # instance attributes
    def __init__(self,id,vmTypeId,priority,starttime,endtime):
        self.id = id
        self.vmTypeId = vmTypeId
        self.priority = priority
        self.starttime = starttime
        self.endtime = endtime
    
    def __repr__(self) -> str:
         rep = 'VM(' +str(self.vmType) + ',' + str(self.core) + ',' + str(self.memory) + ")"
         return rep
