from random import choice
from markdown2 import Markdown
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util 
from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(max_length=64, label='Title:',widget=forms.TextInput(attrs={'class':'form-control'}))
    textarea = forms.CharField(label='Text Area:',widget=forms.Textarea(attrs={'class':'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)
    if not entry is None:
        markdowner = Markdown()
        html = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "html": html,
            "title" : title
        })
    return render(request,"encyclopedia/404.html")
        
def search(request):
    q = request.GET["q"]
    entry = util.get_entry(q)
    if not entry is None:
        return HttpResponseRedirect(reverse('title', args=(q,)))

    else:
        searchmatches = []
        for title in util.list_entries():
            entry = util.get_entry(title)
            if q in entry:
                searchmatches.append(title)
        return render(request, "encyclopedia/query.html",{
                "results": searchmatches
        })

def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                'message': 'New entry added successfully'
            })
        else:
            return render(request, "encyclopedia/create.html",{
                "form" : form
            })

    return render(request, "encyclopedia/create.html",{
        "form" : NewPageForm()
    })

def random(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(reverse('title', args=(title,)))

def edit(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            util.save_entry(title, content)
        else:
            return render(request, "encyclopedia/edit.html", {
                'title':title,
                'form': form
            })
        return HttpResponseRedirect(reverse('title', args=(title,)))
    else:
        form = NewPageForm(initial={'title':title, 'textarea':util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            'title':title,
            'form': form
        })