from .models import Category # import Category model

def menu_links(request):
    
    links = Category.objects.all() # fetch all objects from Category model into variable links
    
    return dict(links=links)