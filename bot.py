from asyncio.windows_events import NULL
from argon2 import PasswordHasher
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import utils
app = Flask(__name__)

'''
'''

def check_exit(message):
    if message=='EXIT':
        utils.new_user_flag = True
        utils.error_flag = False
        utils.bot_state = "" # "form" or "rss"
        utils.form_type = ""
        utils.form_step = -1
        return True
    return False


def get_prompt(type, idx):
    if type=="excision":
        #print(next(iter(utils.items()))[1])
        return utils.excision_prompts.get(str(idx))
    else:
        return ""

@app.route('/bot', methods=['POST'])
def bot():
    if utils.exitnow: quit()
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    exit = check_exit(incoming_msg)
    if exit:
        msg.body("Thank you for using this service. Goodbye.")
        utils.exitnow = True
        return str(msg)
    
    if utils.new_user_flag:
        msg.body("""Hello! Welcome to the Nigerian Land Registration Digital Assistant service. What can I help you with? Please respond with the corresponding menu choice number:
        \n
        1. Help me understand something
        2. Help me fill out a form
        \n
        Send EXIT anytime if you'd like to quit. 
        """)
        utils.new_user_flag = False
        responded = True
    else:       # extending a previous conversation
        if utils.bot_state == "":       # no current main menu item selected
            if incoming_msg == "1":     # resources please
                utils.bot_state = "rss" 
                msg.body("""What would you like help with?""")
                responded = True
            elif incoming_msg == "2":   # forms help
                utils.bot_state = "form"
                utils.form_step = 1
                msg.body("""Which form process would you like to complete? Please respond with the corresponding menu choice number:
                        \n
                        1. Land excision
                        2. Transfer of land ownership
                        3. First-time land registration
                        """)
                responded = True
            

        elif utils.bot_state == "form": 
            if utils.form_step == 1:
                if incoming_msg == "1":
                    utils.form_type = "excision"
                    responded = True
                #elif incoming_msg == "2":
                    #pass    
                #elif incoming_msg =="3":
                #    pass
                #else: 
                    #msg.body("Please enter a valid menu choice.")
          
                if responded:
                    msg.body("""You have selected the land """ + utils.form_type + """ process. We will fill in a form using your responses to following prompts.\n
                    Send EXIT to quit anytime.\n\n""" + get_prompt(utils.form_type, utils.form_step))
                    utils.form_step += 1

            else:
                if utils.form_step == 2:
                    pass
                else:
                    pass
                msg.body(get_prompt(utils.form_type, utils.form_step))
                responded = True
                utils.form_step += 1
















        elif utils.bot_state == "rss":
            if 'process' in incoming_msg:
                msg.body('Here are some helpful links with land processes: https://www.bellanaija.com/2021/12/dennis-isong-excision-of-land-in-nigeria/')
            responded = True

    if not responded:
        msg.body("Please enter a valid input.")
    return str(resp)


if __name__ == '__main__':


    app.run()
