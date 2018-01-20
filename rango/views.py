from django.shortcuts import render

from django.http import HttpResponse # Added by JNR 18.01.2018

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # The key boldmessage is the same as {{ boldmessage}} in the template.
    
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"} # Added by JNR 20.01.2018

    # Return a rendered response to sent to the client.
    # The first parameter is the template to be used.

    return render(request, 'rango/index.html', context=context_dict) # Added by JNR 20.01.2018

# return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") # Added 18.01.2018 and commented out 20.01.2018

def about(request):
    return render(request, 'rango/about.html')
#return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>") # Added 18.01.18
