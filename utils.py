new_user_flag = True
error_flag = False
bot_state = "" # "form" or "rss"
form_type = ""
form_step = 0
exitnow = False
excision_prompts = {"1": "What is your given first name?", "2": "What is your surname?", "3": "What is your date of birth? Please enter in DD/MM/YY format", 
                    "4": "How long have you or your family members lived on your land?", "5": "How large is your household? (Number of people)", 
                    "6": "What are you planning on using the land for?"}
class Person:
    datsa = {"firstname": "", "lastname": "", "age": "", "state_of_origin":"" }

    def __init__(self, dict) -> None:
        self.data = dict