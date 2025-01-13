import requests


ZP_API_REQUEST = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
ZP_API_VERIFY = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"
MERCHANT_ID = "ca8fc811-39b4-409e-96ff-2282b8624883"

def send_request(amount=1000, email="info.test@example.com", phone='09121234567'):
    description = "This Transaction is for test"
    CallbackURL = 'http://127.0.0.1:3000/payment_landing_page'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    amount = 1000 if amount<1000 else amount
    payload = {
        "merchant_id": MERCHANT_ID,  
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {
            "mobile": phone,
            "email": email
        }
    }
    try:
        response = requests.post(ZP_API_REQUEST, json=payload,headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response["data"]['code'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response["data"]['authority']), 'authority': response["data"]['authority']}
            else:
                return {'status': False, 'code': str(response["data"]['code'])}
        return response
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError as e:    
        return {'status': False, 'code': 'connection error'}

# def verify(authority):
#     data = {
#         "MerchantID": MERCHANT_ID,
#         "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
#     response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return {'status': True, 'RefID': response['RefID']}
#         else:
#             return {'status': False, 'code': str(response['Status'])}
#     return response