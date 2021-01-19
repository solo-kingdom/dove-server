# coding: utf-8


def get_remote_ip(request):
    try:
        print(request.META)
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
    except Exception as e:
        print(e)
        ip = ""
    return ip