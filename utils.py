new_user_flag = True
error_flag = False
bot_state = "" # "form" or "rss"
form_type = ""
form_step = 0
exitnow = False
excision_prompts = {"1": "What is your given first name?", "2": "What is your surname?", "3": "What is your date of birth? Please enter in DD/MM/YY format", 
                    "4": "How long have you or your family members lived on your land (in years)?", "5": "How large is your household? (Number of people)", 
                    "6": "What are you planning on using the land for?"}

p_first = ""
p_last = ""
p_DOB = ""
p_YOL = ""
p_numfam = ""
p_landplan = ""
class Person:
    datsa = {"firstname": "", "lastname": "", "age": "", "state_of_origin":"" }

    def __init__(self, first_name) -> None:
        #self.data = dict
        self.firstName = first_name
