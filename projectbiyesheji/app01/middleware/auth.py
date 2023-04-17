from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect

class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        if request.path_info=='/login/':
            return
        #读取当前访问用户的session信息
        info_dict=request.session.get('info')
        if info_dict:
            return 
        #没有登陆
        return redirect('/login/')