import json 



# What user will see on menu
save_display = {
    "Save": 1,
    "Character Name" : "",
    "Progress" : None,
    "Playtime" : 0, 
    "Timestamp" : None,
    "Location" : "Nazareth" 
}


# Actual save data program needs to parse 
save_data = {
    "Progress" : {
        "Level": None, 
        "Easter Eggs" : None,
        "Gospel" : {
            "Chapter" : None
        }
    
    
        
    }
    
    
    
    
    
}






print(json.dumps(save_display, indent=4))

save_file = {
    "display" : save_display, 
    "data" : save_data
}

with open("saves.json", "w") as file:
    json.dump(save_file, file, indent=4)