from functools import wraps
from django.shortcuts import redirect

def survey_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get("survey_complete") is True:
            return view_func(request, *args, **kwargs)
        return redirect('survey')
    return _wrapped_view