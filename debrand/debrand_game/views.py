from django.shortcuts import render, redirect
from .models import Player, Level, GameObject
from .forms import PlayerForm


def character_customization_view(request):
    """
    A form is used to name and create a new character. The player will be stored within the database, and player ID
    stored in cookies for this playthrough.
    https://tutorial.djangogirls.org/en/django_forms/
    :param request:
    :return:
    """

    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.save()
            # https://docs.djangoproject.com/en/3.0/topics/http/sessions/
            request.session['player_id'] = player.id  # save player's ID in session for future levels.
            return redirect('level', level_slug='beginning')
    else:
        form = PlayerForm()
        return render(request, 'char_customize.html', {'form': form})


def leaderboard_view(request):
    """
    Lists all past players in a leaderboard style table.
    :param request:
    :return:
    """
    context = {}
    return render(request, 'leaderboard.html', context)


def level_view(request, level_slug="beginning"):
    """
    This is a generic view that fills content based on the level's URL slug.
    URL slug gets the object with that slug and populates the context.

    Game over view is also handled here, since the description content generally covers the consequences of the last
    level's decisions.

    Using: https://github.com/agusmakmun/django-markdown-editor for Markdown.
    :param request:
    :param level_slug:
    :return:
    """
    try:
        player = Player.objects.get(id=request.session.get('player_id'))
    except:  # if no player with that ID, redirect to title screen
        redirect('title')

    # get this level.
    level_object = Level.objects.get(slug=level_slug)
    buttons = level_object.get_next_buttons()
    # my_obj.categories.add(fragmentCategory.objects.get(id=1))
    context = {
        'playername': player.name,
        'img_src': level_object.img_src,
        'name': level_object.name,
        'description': level_object.description,
        'buttons': buttons
    }
    return render(request, 'level.html', context)


