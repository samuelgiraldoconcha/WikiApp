import markdown2
from django.shortcuts import render, redirect
from django.http import HttpResponse
from encyclopedia.util import get_entry, save_entry
from . import util
from django import forms
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entries(request, TITLE):
    entry_content = get_entry(TITLE)

    if entry_content is None:
        # Handle case where entry is not found
        return render(request, 'encyclopedia/not_found.html')

        # Convert Markdown content to HTML
    html_content = markdown2.markdown(entry_content)

    return render(request, 'encyclopedia/entry.html', {
        'html_content': html_content,
        'title': TITLE
        })

def search_results(request):
    query = request.GET.get("q")
    found_entries = []
    for entry in util.list_entries():
        if query.lower() in entry.lower():
            found_entries.append(entry)
        elif query.lower() is entry.lower():
            return display_entries(request=request, TITLE=query)
    return render(request, 'encyclopedia/search_results.html', {
        "entries": found_entries
    })

def create_new_entry(request):

    form = NewEntryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']

        existing_entry = get_entry(title)
        if existing_entry is not None:
            messages.error(request, f"An entry with the title '{title}' already exists.")
            return render(request, 'encyclopedia/new_entry.html', {'form': form})

        save_entry(title, content)
        return display_entries(request, title)

    return render(request, 'encyclopedia/new_entry.html', {'form': form})

def modify_entry(request, title):

    content = get_entry(title)  # Fetch existing content based on the entry title

    if request.method == 'POST':
        new_content = request.POST.get('new_content')  # Get the updated content from the form
        # Save the updated content to the entry (use your utility function to save)
        save_entry(title, new_content)
        # Redirect the user back to the entry's page
        return redirect('display_entries', title)

    return render(request, 'encyclopedia/modify_entry.html', {'title': title, 'content': content})  

def random_entry(request):
    all_entries = util.list_entries()  # Retrieve all entry titles
    random_entry = random.choice(all_entries)  # Choose a random entry from the list

    return redirect('display_entries', random_entry)

def Samuel(request):
    return render(request, "encyclopedia/samuel.html")

