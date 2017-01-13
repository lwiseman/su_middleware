from django.views.generic import TemplateView

class SetSessionView(TemplateView):
    template_name = 'testsessions/testsessions.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        request.session['test'] = 'fart'
        return self.render_to_response(context)
