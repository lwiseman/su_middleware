from importlib import import_module

from django.conf import settings
from django.contrib.auth import authenticate, get_user, login

engine = import_module(settings.SESSION_ENGINE)
SessionStore = engine.SessionStore

def su_middleware(get_response):
    def context_switch(request, session_key):
        request.session = SessionStore(session_key)
        request.user = get_user(request)
    def middleware(request):
        is_suing = request.user.is_authenticated() and ('su' in request.GET or 'su_sessionid' in request.session) # and <permission check>
        if is_suing:
            orig_session = curr_session = request.session
            while 'su_sessionid' in request.session:
                context_switch(request, request.session['su_sessionid'])
                curr_session = request.session
            if request.GET.get('su'):
#            # rotate_token(request) TODO: seemed to have same csrf token
                request.session = SessionStore()
                request.session['prev_su_sessionid'] = curr_session.session_key
                login(request, authenticate(remote_user=request.GET['su']))
                curr_session['su_sessionid'] = request.session.session_key
                curr_session.save() # TODO: duplicate save after response if first su in chain, also why does exit or setting session values on su'ed accounts sometimes not trigger a cookie update, but su always does?
        if 'exit' in request.GET and 'prev_su_sessionid' in request.session:
            context_switch(request, request.session['prev_su_sessionid'])
            del request.session['su_sessionid']
        response = get_response(request)
        if is_suing:
            request.session.save() # TODO: check if new_session has been modified (or there's been an exit?) instead of blindly saving
            request.session = orig_session
        return response
    return middleware
