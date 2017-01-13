from importlib import import_module

from django.conf import settings
from django.contrib.auth import authenticate, get_user, login

def su_middleware(get_response):
    def middleware(request):
        is_suing = request.user.is_authenticated() and ('su' in request.GET or 'su_sessionid' in request.session) # and <permission check>
        if is_suing:
            engine = import_module(settings.SESSION_ENGINE)
            SessionStore = engine.SessionStore
            old_session = request.session
            if request.GET.get('su'):
# OPTION 1: try to provide brand new session, but previous sessions are flushed on login... rewrite request.session.session_key?
#            user = authenticate(remote_user=suing)
#            login(request, user)
#            # rotate_token(request) TODO: seemed to have same csrf token
# OPTION 2: swap out user (works, but session vars overlap)
#            request.user = authenticate(remote_user=suing)
#            request.session[SESSION_KEY] = request.user._meta.pk.value_to_string(request.user)
#            request.session[HASH_SESSION_KEY] = session_auth_hash
# OPTION 3: give new session, have to make sure that on next request user from sessionid in cookie matches REMOTE_USER from downstream or RemoteUserMiddleware does stuff
#            new_session = SessionStore()
#            new_session.save()
                request.session = SessionStore()
                login(request, authenticate(remote_user=request.GET['su']))
                old_session['su_sessionid'] = request.session.session_key
            else:
                request.session = SessionStore(request.session['su_sessionid'])
                request.user = get_user(request)
        response = get_response(request)
        if is_suing:
            request.session.save() # TODO: check if new_session has been modified instead of blindly saving
            request.session = old_session
        return response
    return middleware
