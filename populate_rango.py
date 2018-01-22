import os # Created by JNR 22.01.2018
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

# Create a list of dictionaries containing the pages to add to each category.
# Also dictionary of dictionaries for the categories.
# It allows iteration through each data structure and add the data.

    python_pages = [
        {"title": "Official Python Tutorial",
        "url": "http://docs.python.org/2/tutorial/"},
        {"title": "How to Think Like a Computer Scientist",
        "url": "http://www.greenteapress.com/thinkpython/"},
        {"title": "Learn Python in 10 Minutes",
        "url": "http://www.korokithakis.net/tutorials/python/"}
        {"views": 128}]

    django_pages = [
        {"title": "Official Django Tutorial",
        "url": "http://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title": "Django Rocks",
        "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django",
        "url": "http://www.tangowithdjango.com/"}]

    other_pages = [
        {"title": "Bottle",
        "url": "http://bottlepy.org/docs/dev/"},
        {"title": "Flask",
        "url": "http://flask.pocoo.org"}]

    cats = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages}}

# If you want to add more categories or pages, add them to the dictionaries above.

# The code below goes through the cats dictionary then adds each category.
# http://docs.quantifiedcode.com/python-anti-patterns/readability/ for more info.

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data["pages"]:
            add_page(c, p ["title"], p["url"])

    # Print out the categories we have added

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print ("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title) [0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0): # Modified by JNR 22.01.2018
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views # Added by JNR 22.01.2018
    c.likes=likes # Added by JNR 22.01.2018
    c.save()
    return c

# Start execution here

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
