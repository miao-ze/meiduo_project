from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from utils.response_code import RETCODE


"""自定义判断用户是否登录的扩展类：返回JSON"""
class LoginRequiredJSONMixin(LoginRequiredMixin):

    # 为什么只需要重写handle_no_permission方法？
    # 因为判断用户是否登录的操作，父类已经完成，子类只需要关心，如果用户为登录，对应怎么操作
    # 而，handle_no_permission方法就是未登录时，要执行的方法
    def handle_no_permission(self):
        """直接响应JSON数据"""
        return JsonResponse({'code':RETCODE.SESSIONERR,'errmsg':'用户未登录'}) #code:'4101'



"""
class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            当用户未登录时会执行：handle_no_permission方法
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
        
原handle_no_permission方法
def handle_no_permission(self):
    if self.raise_exception or self.request.user.is_authenticated:
        raise PermissionDenied(self.get_permission_denied_message())

    path = self.request.build_absolute_uri()
    resolved_login_url = resolve_url(self.get_login_url())
    # If the login url is the same scheme and net location then use the
    # path as the "next" url.
    login_scheme, login_netloc = urlsplit(resolved_login_url)[:2]
    current_scheme, current_netloc = urlsplit(path)[:2]
    if (not login_scheme or login_scheme == current_scheme) and (
        not login_netloc or login_netloc == current_netloc
    ):
        path = self.request.get_full_path()
    return redirect_to_login(
        path,
        resolved_login_url,
        self.get_redirect_field_name(),
    )
"""


