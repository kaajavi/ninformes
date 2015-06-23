from django.shortcuts import render_to_response
from django.template import RequestContext



def view_create_principal(request):
    context = RequestContext(request)                
    return render_to_response('testing/test_create_principal.html', {},context)



###para cfk
from django import forms
from ckeditor.widgets import CKEditorWidget


class ExampleCFKForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())

def test_cfkeditor(request):
    context = RequestContext(request)                
    form = ExampleCFKForm()
    return render_to_response('testing/test_cfkeditor.html', {'form':form},context)