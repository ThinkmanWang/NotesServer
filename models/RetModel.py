
class RetModel(object):
    code = 0;
    message = ""
    
    def __init__(self, code=0, message="", data=None):
        self.code = code
        self.message = message
        self.data = data