"""Modules"""
import random
import re
import markdown2

# Django functions
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Lokal functions
from . import util
from .forms import NewPageForm, EditPageForm


def index(request):
    """Index with a list of all entries"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, titel):
    """Convert markup text to HTML, view entry """
    content = util.get_entry(titel)
    if content is not None:
        content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "content": content,
        "titel": titel
    })


def search(request):
    """Search for entries"""
    # Get user input form (layout.html)
    query_dict = request.GET
    qurey = query_dict.get("q")
    entries = util.list_entries()

    if qurey in entries:
        url = reverse("view_entry", args={qurey})
        return HttpResponseRedirect(url)

    # Search the titles of all entries
    pattern = re.compile(re.escape(qurey), re.IGNORECASE)
    results = list(filter(pattern.search, entries))

    return render(request, "encyclopedia/search.html", {
        "results": results
        })


def new(request):
    """Create a new entry"""
    if request.method == "POST":
        # Get user submitted data
        form = NewPageForm(request.POST)

        if form.is_valid():
            # Get the cleaned data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Save the entry using the premade cs50W funktion
            util.save_entry(title, content)

            # Go to view_entry of the new page
            url = reverse("view_entry", args={title})
            return HttpResponseRedirect(url)

        # If titel is alredy used, go to form with the data and error message.
        return render(request, "encyclopedia/new.html", {
            "form": form
        })

    # When the user enters the url via get show an emty form
    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })


def edit(request):
    """Edit an exixting entry"""
    if request.method == "POST":
        # Get the data
        form = EditPageForm(request.POST)
        if form.is_valid():
            # Get the cleaned data
            titel = form.cleaned_data["titel"]
            content = form.cleaned_data["content"]
            util.save_entry(titel, content)
            # Go to view_entry of the edited page
            url = reverse("view_entry", args={titel})
            return HttpResponseRedirect(url)

    else:
        titel_dict = request.GET
        titel = titel_dict.get("titel")
        content = util.get_entry(titel)
        form = EditPageForm(initial={"content": content, "titel": titel})

        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "titel": titel
        })


def view_random(request):
    """Go to a random page"""
    entry_list = util.list_entries()
    titel = random.choice(entry_list)
    url = reverse("view_entry", args={titel})
    return HttpResponseRedirect(url)
