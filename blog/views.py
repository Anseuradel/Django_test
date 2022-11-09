from django.shortcuts import render
from .models import Post
from .models import Algo
from django.views.generic import TemplateView

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def test(request):
    context = {
        ' algos': Algo.objects.all()
    }
    return render(request, 'blog/about.html', context)

def liste_dispatch(x,marge):
    DFT_sorted = x.sort_values(by =["ratio"],ascending = False)
    toBeInvoked = []
    index1 = 0
    while (index1  < len(DFT_sorted)) :
        index2 = index1 + 1
        origin_index1 = DFT_sorted.index[index1]
        exclude = False
        while (index2  < len(DFT_sorted)): 
            origin_index2 = DFT_sorted.index[index2]
            c = (DFT_sorted["ratio"][origin_index1] - DFT_sorted["ratio"][origin_index2])
            if(c >= marge):
                exclude = True
                break;
            index2 = index2 + 1    
        if(exclude == False):
            toBeInvoked.append(origin_index1) 
        index1 = index1 + 1
    return(toBeInvoked)