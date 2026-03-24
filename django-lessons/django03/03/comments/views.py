from django.shortcuts import render
from .models import Comment

def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'comments/list.html', {'comments': comments})