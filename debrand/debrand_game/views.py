from django.shortcuts import render, redirect, reverse
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
    # todo: handle player and non-player use cases
    player_id = request.session.get('player_id', False)
    player = Player.objects.get(player_id)
    players_who_completed = Player.objects.filter(completed=True)
    context = {
        'players': players_who_completed,
        'player_id':player_id
    }
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
        return redirect('title')

    # get this level.
    try:
        level_object = Level.objects.get(slug=level_slug)
    except:
        # no next level so redirect to end
        player.set_completed()
        return redirect('leaderboard')

    if level_object.has_next():
        buttons = level_object.get_next_buttons()
    else:
        buttons = [("See results", reverse('leaderboard')),]

    player.levels_played.add(level_object)  # add this level to the list of played levels (saves automatically)
    player.update_score()  # and update the score. todo: add a UI element for the score. SIDEBAR.

    context = {
        'playername': player.get_name(),
        'img_src': level_object.get_img_src(),
        'name': level_object.name,
        'description': level_object.get_description(),
        'buttons': buttons,
        'score': player.get_score()
    }
    return render(request, 'level.html', context)

