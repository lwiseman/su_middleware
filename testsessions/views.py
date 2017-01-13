from django.views.generic import TemplateView

class ExitView(TemplateView):
    template_name = 'testsessions/testsessions.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        del request.session['su_sessionid']
        return self.render_to_response(context)

class SetSessionView(TemplateView):
    template_name = 'testsessions/testsessions.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        request.session.update(request.GET)
        return self.render_to_response(context)
