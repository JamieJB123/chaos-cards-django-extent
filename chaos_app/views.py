import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Card
from .forms import CardForm

# Views

# Home page view

def home(request):
    """Render the home page of the application.
    Home view differs depending on authentication status:
    - If the user is authenticated, see a basic home page with option
    to play the game.
    - If the user is not authenticated, they see a more descriptive
    home page with option to register or log-in.
    This is handled in the template.
    """
    return render(request, 'chaos_app/home.html', {
        # Flag to indicate if the spin button has been pressed
        'spin_attempted': False,
    })

# Random Card Generator View

@login_required
def random_card_view(request):
    """
    Display a random card from the user's collection.
    If the user has no cards, display a message indicating that.
    If the user has cards, select one at random and display it.

    **Context**
        random_card (Card): The randomly selected card instance, or None if no cards exist.
        spin_attempted: A boolean flag indicating whether a spin was attempted (used to determine home page display).

    **Template**
        chaos_app/home.html
    """
    user_cards = Card.objects.filter(user=request.user)
    if user_cards.exists():
        # Select a random card if cards exist
        random_card = random.choice(user_cards)
        # Set a flag to indicate that a spin was attempted
        spin_attempted = True
    else:
        # Set to None if no cards exist
        random_card = None
        # Still set the flag to indicate a spin was attempted
        spin_attempted = True

    return render(request, 'chaos_app/home.html', {
        'random_card': random_card,
        # Pass the flag to the template
        'spin_attempted': spin_attempted,
    })

# Card list view

@login_required
def user_cards_view(request):
    """
    Display a list of cards created by the logged-in user.
    The cards are ordered by the date they were created, in descending order.
    Page is paginated. If >= 10 cards exist, show pagination controls.
    If the user submits a form to create a new card, it is processed, saved and displayed.

    **Context**
        form (CardForm): The form for creating a new card.
        cards (QuerySet): The paginated list of cards created by the user.
        is_paginated (bool): Indicates whether pagination is applied.
        page_obj (Page): The current page object for pagination.

    **Template**
        chaos_app/user_cards.html
    """
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.add_message(request, messages.SUCCESS,
            'Card created successfully!')
            return redirect('user_cards')
        else:
            messages.add_message(request, messages.ERROR,
            'Error creating card. Please try again.')
    else:
        form = CardForm()

    user_cards = Card.objects.filter(user=request.user).order_by('-created_on')
    paginator = Paginator(user_cards, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'chaos_app/user_cards.html', {
        'form': form,
        'cards': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    })

@login_required
def edit_card_view(request, card_id):
    """
    Edit an existing card created by the logged-in user.
    If the card is successfully edited a message is displayed.

    **Context**
        form (CardForm): The form for editing the card.
        card (Card): The card instance being edited.

    **Template**
        chaos_app/user_cards.html
    """
    card = get_object_or_404(Card, id=card_id, user=request.user)
    if request.method == "POST":
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.add_message(request, messages.SUCCESS,
            "Card updated successfully!")
            return redirect('user_cards')
        else:
            messages.add_message(request, messages.ERROR,
            "Error updating card. Please try again.")
    return redirect('user_cards')

@login_required
def delete_card_view(request, card_id):
    """
    Delete an existing card created by the logged-in user.
    If the card is successfully deleted, a success message is displayed.

    **Context**
        card (Card): The card instance being deleted.

    **Template**
        chaos_app/user_cards.html
    """
    card = get_object_or_404(Card, id=card_id, user=request.user)
    if card:
        card.delete()
        messages.add_message(request, messages.SUCCESS,
        "Card deleted successfully!")
    else:
        messages.add_message(request, messages.ERROR,
        "Error deleting card. Card not found.")
    return redirect("user_cards")
