import random, json
from redis import Redis

class OTPCode():

    @classmethod
    def run_redis(cls):
        redis_client = Redis(host='localhost', port=6379, db=0)
        return redis_client

    @classmethod
    def save_otp_to_redis(cls, email, otp_code):
        redis_client = cls.run_redis()
        redis_client.set(f'otp_{email}', otp_code, ex=600)
        

    @classmethod
    def save_user_data_to_redis(cls, email, data):
        redis_client = cls.run_redis()
        data_json = json.dumps(data)
        redis_client.set(f'user_data_{email}', data_json, ex=600)
    
    @classmethod
    def get_otp_code(cls, email):
        redis_client = cls.run_redis()
        return redis_client.get(f'otp_{email}')
    
    @classmethod
    def get_user_data(cls, email):
        redis_client = cls.run_redis()
        user_data = redis_client.get(f'user_data_{email}')
        if user_data:
            return json.loads(user_data.decode()) 
        return None

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))
    
    @classmethod
    def save_authority_to_redis(cls, authority, order_id):
        redis_client = cls.run_redis()
        redis_client.set(f'authority_{authority}', order_id, ex=600)

    @classmethod
    def get_order_id_by_authority(cls, authority):
        redis_client = cls.run_redis()
        order_id = redis_client.get(f'authority_{authority}')
        if order_id:
            return order_id.decode()
        return None