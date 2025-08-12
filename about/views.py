from django.shortcuts import render, redirect
from django.contrib import messages
from .models import About
from .forms import FeedbackForm


# Create your views here.
def about(request):
    """
    Returns the 'about' model content created by the superuser to be displayed as the about section in about/about.html. Also returns the feedback form for users to submit their messages.

    Handles feedback form submissions. If form is valid the form is saved to the database, the user sees a success message and is redirected to the about template. If form is invalid the user sees an error message.

    **Context**
        about (About): The latest About model instance.
        form (FeedbackForm): The feedback form instance.

    **Template**
        about/about.html
    """

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Contact form sent successfully!")
            return redirect('about')
        else:
            messages.add_message(request, messages.ERROR, "Error sending contact form. Please try again.")

    about = About.objects.all().order_by("-updated_on").first()
    form = FeedbackForm()

    return render(request, 'about/about.html', {
        'about': about,
        'form': form,
    })
