from asyncio.windows_events import NULL
from argon2 import PasswordHasher
from flask import Flask, request
from graphql import do_types_overlap
import requests
from twilio.twiml.messaging_response import MessagingResponse
import utils
import sqlite3
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
def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

def makedb():
    connection = sqlite3.connect('applications.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Applications
                (id integer PRIMARY KEY, FirstName TEXT, LastName TEXT, DOB TEXT, YEARS_ON_LAND TEXT, SIZE_OF_HOUSEHOLD TEXT, LAND_PLANS TEXT)''')

    connection.commit()
    connection.close()

@app.route('/bot', methods=['POST'])
def bot():
   # makedb()
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
                if utils.form_step == 2:    # first name
                    utils.p_first = incoming_msg
                    
                elif utils.form_step == 3:  # last name, prompt dob
                    utils.p_last = incoming_msg
                    
                elif utils.form_step == 4:  # dob
                    utils.p_DOB = incoming_msg
                elif utils.form_step == 5:  # years lived on land
                    utils.p_YOL = incoming_msg
                elif utils.form_step == 6:  # size of household
                    utils.p_numfam = incoming_msg
                elif utils.form_step == 7:  # what you're using the land for
                    utils.p_landplan = incoming_msg
                    try:
                        conn = sqlite3.connect('applications.db')
                        #print('h1')
                        cur = conn.cursor()
                        #print('h2')
                        insert_users = ''' INSERT INTO Applications(id, FirstName, LastName, DOB, YEARS_ON_LAND, SIZE_OF_HOUSEHOLD, LAND_PLANS) 
                        VALUES(?,?,?,?,?,?,?) '''
                        cur.execute(insert_users, [1, utils.p_first, utils.p_last, utils.p_DOB, utils.p_YOL, utils.p_numfam, utils.p_landplan])
                        #print('h3')
                        conn.commit()
                        #print('h4')
                        responded = True
                        msg.body('Thanks for sending your info! Your form has been completed and sent to the Land Registry.') 
                    except sqlite3.Error as e:
                        print(e)
                    finally:
                        if conn:
                            conn.close()
               
                if utils.form_step < 7:   
                    msg.body(get_prompt(utils.form_type, utils.form_step))
                    responded = True
                    utils.form_step += 1



        elif utils.bot_state == "rss":
            if 'process' in incoming_msg:
                msg.body('Here are some helpful links with land processes: https://www.bellanaija.com/2021/12/dennis-isong-excision-of-land-in-nigeria/')
                responded = True
            if 'verified' in incoming_msg:
                msg.body('List of verified quantity surveyors in Nigeria: https://www.finelib.com/cities/lagos/business/construction/surveyors')
                responded = True
            if 'document' in incoming_msg:
                msg.body('Document required for land registration in Nigeria: https://www.lexology.com/library/detail.aspx?g=fcab8ae2-60b8-4ce6-ab98-af514634843b')
                responded = True
    if not responded:
        msg.body("Please enter a valid input.")
    return str(resp)


if __name__ == '__main__':
    makedb()
    app.run()
