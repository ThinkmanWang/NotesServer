class User(object):
    id = 0
    user_name = ''
    password = ''
    token = ""
    create_time = 0
    expire_time = 0
        
    def __init__(self, id=0, user_name="", password="", token="", create_time=0, expire_time=0):
        self.id = id
        self.user_name = user_name
        self.password = password    
        self.token = token
        self.create_time = create_time
        self.expire_time = expire_time
    