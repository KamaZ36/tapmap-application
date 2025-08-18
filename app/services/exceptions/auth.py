from app.domain.exceptions.base import AppException


class InvalidAccessToken(AppException): 
    pass

class ExpiredAccessToken(AppException):
    pass
    
class NoAccess(AppException):
    pass   
