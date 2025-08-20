from django.shortcuts import render
from edit_images.models import Image

def index(request):
    """
    Render the index page.
    """
    images_list = Image.objects.order_by('-created_at')[:10]
    context = {"images_list": images_list}
    return render(request, 'index.html', context)
