class VM:
     # instance attributes
    def __init__(self,type,core,memory):
        self.vmTypeId = type
        self.core = core
        self.memory = memory
    
    def __repr__(self) -> str:
         rep = 'VM(' +str(self.vmTypeId) + ',' + str(self.core) + ',' + str(self.memory) + ")"
         return rep


    
