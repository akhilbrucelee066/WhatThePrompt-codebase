from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "promptpedia/index.html", 
{"entries": util.list_entries()})

def entry(request, title):
    if title in util.list_entries():
        return render(request, "promptpedia/entry.html", {"title": title, "entry": util.get_entry(title)})
    return render(request, "promptpedia/error.html", {"title": title})

def search(request):
    if request.method == "POST":
        query = request.POST.get("q", "").strip()
        entries = util.list_entries()
        if query in entries:
            return redirect("entry", title=query)
        else:
            results = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "promptpedia/search_results.html", {
                "query": query,
                "results": results
            })
            
def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        
        if not title or not content:
            return render(request, "promptpedia/error.html", {
                "message": "Title and content are required."
            })
            
        if title in util.list_entries():
            return render(request, "promptpedia/error.html", {
                "message": f"Entry '{title}' already exists."
            })
            
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "promptpedia/create.html")
