class h5file:
    def __init__(self, filename):
        """Class initialization"""
        f = h5py.File(filename, 'r')
        allkeys = []
        f.visit(allkeys.append)
        allkeys.sort()
        keys = [key for key in allkeys if isinstance(f[key], h5py.Dataset)]
        
        self.filename = filename
        self.f = f
        self.allkeys = allkeys
        self.keys = keys
    
    def matchkeys(self, getkey):
        return [key for key in self.keys if getkey in key]
    
    def index(self, key):
        matching_keys = self.matchkeys(key)
        if len(matching_keys) == 1:
            return self.f[matching_keys[0]]
        elif len(matching_keys) > 1:
            raise Exception("{} matches found: {}".format(len(matching_keys),
                                                         matching_keys))
        elif len(matching_keys) == 0:
            raise Exception("{} not found".format(key))
        return
    
    def get_description(self):
        description = 'Filename is: {} \nKeys are:\n'.format(self.filename)
        description += "\n".join(self.keys) + '\n'
        return description
 
    def __str__(self):
        return self.get_description()

    def __repr__(self):
        return self.get_description()
    
    def __getitem__(self, key):
        return self.index(key)
