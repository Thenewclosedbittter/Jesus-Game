import json 
import pickle 


display_data = {
    "Time Played" : (0, 0, 0), 
    "Location" : "None", 
    "Name" : None
}



class savesys:
    def __init__(self, save_folder):
        self.json = json
        self.save_folder = save_folder
    def save(self, data, name):
        data_file = open(self.save_folder+"/"+name+self.json, "wb")
        pickle.dump(data, data_file)
    def load_data(self, name):
        data_file = open(self.save_folder+"/"+name+self.file_extension, "rb")
        data = pickle.load(data_file)
        return data
    
    
Save = savesys("saves")
