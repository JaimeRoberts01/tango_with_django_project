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
# UserForm and UserProfileForm
from rango.forms import UserForm, UserProfileForm # Added by JNR 20.01.2018
# Others
from django.contrib.auth import authenticate, login # Added by JNR 29.01.2018
from django.http import HttpResponseRedirect, HttpResponse # Added by JNR 29.01.2018
from django.core.urlresolvers import reverse # Added by JNR 29.01.2018
# Login required
from django.contrib.auth.decorators import login_required # Added by JNR 29.01.2018
# Logout
from django.contrib.auth import logout # Added by JNR 29.01.2018

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

# ----------------------------------------------------------- #

def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to # True when registration succeeds.

    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

    # Grab information from the raw form information - makes use of both UserForm and UserProfileForm.

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Hash the password with the set_password method.
            # Once hashed, we can update the user object.

            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in UserProfile model.

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.

            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP POST, so render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.

        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                    'rango/register.html',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered})

# ----------------------------------------------------------- #

def user_login(request):
    # If the request is a HTTP POST, pull out the relevant information.
    if request.method == 'POST':
        # Get the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. Can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

# ----------------------------------------------------------- #

@login_required # Added by JNR 29.01.2018
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html', {}) # Added by JNR 29.01.2018
# ----------------------------------------------------------- #

@login_required # Added by JNR 29.01.2018
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))




