import json 
import pickle 


user_new = True 

if user_new:
	new = "New"


# Data displayed to user 
display_data = {
    "Time Played" : (0, 0, 0), 
    "Location" : "None", 
    # When it is a new save, only the name will be displayed for the user to input. Otherwise, all the other information will be outputed. 
    "new_save" : {"Name" : None}
}

def data_display():	
	# Final string 
	game_save = "" 
	if user_new: 
		name = display_data["new_save"]["Name"]
		game_save = "Name:"
		game_save = game_save.ljust(18)
	else:
		for key, value in display_data.new_save.items():
			game_save += f"{key}: "
			game_save += "\n"
	return game_save



