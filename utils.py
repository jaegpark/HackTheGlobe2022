new_user_flag = True
error_flag = False
bot_state = "" # "form" or "rss"
form_type = ""

class Person:
    data = {"firstname": "", "lastname": "", "age": "", "state_of_origin":"" }

    def __init__(self, dict) -> None:
        self.data = dict