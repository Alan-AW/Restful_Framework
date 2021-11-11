class SVIPPermission(object):
    massage = 'SVIP才能访问本页面'
    def has_permission(self, request, view):
        if request._request.user.user_type != 3:
            return False
        return True
