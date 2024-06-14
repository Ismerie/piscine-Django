from django.shortcuts import render
from .forms import EntryForm
import os
from datetime import datetime

def entry(request):
    log_file = os.path.join(os.path.dirname(__file__), 'log.txt')
    
    if request.method == "POST":
        form = EntryForm(request.POST)
        
        if form.is_valid():
            entry = form.cleaned_data['entry']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(log_file, 'a') as f:
                    f.write(f"{timestamp}: {entry}\n")
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier de logs : {e}")
    else:
        form = EntryForm()   

    entries = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                entries = f.readlines()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier de logs : {e}")

    context = {
        'form': form,
        'entries': entries,
    }

    return render(request, 'entry.html', context)

# Create your views here.
