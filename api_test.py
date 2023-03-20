import requests

def log_out(user_id, premise_id):
    response = requests.post('https://pehchaan.grjcodes.com/api/log_out.php', data={'uid':user_id,'premise_id':premise_id})
    print(response.text)
def log_in(user_id, premise_id):
    response = requests.post('https://pehchaan.grjcodes.com/api/log_in.php', data={'uid': user_id, 'premise_id': premise_id})
    print(response.text)
log_in('2019CMPN30', 'B31')