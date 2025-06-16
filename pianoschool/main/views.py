from django.shortcuts import render, redirect


def index(request):
    return render(request, 'main/index.html')


def modal(request):
    return render(request, 'main/modal.html')

def klavesin(request):
    return render(request, 'main/klavesin.html')
def organ(request):
    return render(request, 'main/organ.html')




