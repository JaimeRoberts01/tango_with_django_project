from django.shortcuts import render
from django.http import HttpResponse # Added by JNR 18.01.2018
# Import the category model
from rango.models import Category # Added by JNR 23.01.2018
# Import the page model
from rango.models import Page # Added by JNR 23.01.2018
# CategoryForm
from rango.forms import CategoryForm # Added by JNR 23.01.2018
# PageForm
from rango.forms import PageForm # Added by JNR 23.01.2018

# ----------------------------------------------------------- #

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # The key boldmessage is the same as {{ boldmessage}} in the template.

    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"} # Added by JNR 20.01.2018 and commented out 23.01.2018

    # Return a rendered response to sent to the client.
    # The first parameter is the template to be used.
    # Retrieve the top 5 only or all if less than 5.
    # Palce the list in the contect_dict dictionatry to pass to the template engine.

    category_list = Category.objects.order_by('-likes') [:5] # Added by JNR 23.01.2018
    page_list = Page.objects.order_by('-views') [:5]
    context_dict = {'categories': category_list, 'pages':page_list}

# return render(request, 'rango/index.html', context=context_dict) # Added by JNR 20.01.2018 and commented out 23.01.2018

    return render(request, 'rango/index.html', context_dict)

# return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") # Added 18.01.2018 and commented out 20.01.2018

# ----------------------------------------------------------- #

def about(request):

    # Query the database for a list of ALL categories currently stored.

    return render(request, 'rango/about.html')
#return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>") # Added 18.01.18

# ----------------------------------------------------------- #

def show_category(request, category_name_slug): # Added by JNR 23.01.2018
    # Create a context dictionary that can be passed to the template rendering engine.
    context_dict = {}

    try:
        # If can't find a category bane slug then the .get method raises a DoesNotExist exception.
        # It returns one model instance or raises an exception.

        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages. filter() will return a list of of objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Adds our restils list to the template comtext under name pages.
        context_dict['pages'] = pages
        # Also add the category onject from the database to the context dictionary.
        # Used in the template to verify the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # The template will display the "no category" maessage.
        context_dict['category'] = None
        context_dict['pages'] = None

        # Render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

# ----------------------------------------------------------- #

def add_category(request):
    form = CategoryForm()

    # A HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            print(cat, cat.slug)

            # Now that the category is saved, we could give a confirmation message
            # But since the most recent category added is on the index page, we can
            # direct the user back to the index page.

            return index(request)
        else:
            # The supplied form contained errors so just print them to the terminal.
            print(form.errors)

    # This will handle the bad form, new form or no form supplied cases.
    # Render the form with error messages if there are any.

    return render(request, 'rango/add_category.html', {'form': form})

# ----------------------------------------------------------- #

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
