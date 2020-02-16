from django.db import models
from django.template.defaultfilters import slugify
from martor.models import MartorField

class GameObject(models.Model):
    """
    A GameObject is something that the player encounters within a Level.
    Players' scores will be determined by what they choose within each level and which GameObjects are within.
    """

    name = models.CharField(max_length=96)
    slug = models.SlugField(unique=True, blank=True)
    variety = models.CharField(choices=[
            ('UN', "Unseen"),
            ("P", "Poop"),
            ("A", "Advertisement"),
            ("E", "Emergency")
        ],
        max_length=2
    )
    points = models.IntegerField()  # how many points this object is worth

    def __str__(self):
        return self.slug

    def __repr__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        This method populates slug on first save.
        :param args:
        :param kwargs:
        :return:
        """
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        return super(GameObject, self).save(*args, **kwargs)


class Level(models.Model):
    """
    A level is equivalent to a scene. It contains GameObjects. The whole "game" is made up of a series of Level.

    """
    name = models.CharField(max_length=96)
    slug = models.SlugField(unique=True, blank=True)
    game_objects = models.ManyToManyField(GameObject)
    next_levels = models.ManyToManyField("self", symmetrical=False, blank=True)
    description = MartorField()
    button_text = models.CharField(max_length=60)  # this goes on the buttons for when this is a next level
    img_src = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.slug

    def __repr__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        This method populates slug on first save.
        :param args:
        :param kwargs:
        :return:
        """
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        return super(Level, self).save(*args, **kwargs)

    def get_next_levels(self):
        return self.next_levels

    def get_next_button_text(self):
        return [level.button_text for level in self.next_levels.all()]

    def get_next_slugs(self):
        return [level.slug for level in self.next_levels.all()]

    def get_next_buttons(self):
        return list(zip(self.get_next_button_text(),self.get_next_slugs()))

    def get_description(self):
        return self.description

    def get_game_objects(self):
        return self.game_objects

    def get_points(self):
        return sum([game_object.points for game_object in self.game_objects.all()])


# Create your models here.
class Player(models.Model):
    """
    This Player tracks the player's progress through the game.
    """
    name = models.CharField(max_length=96)
    slug = models.SlugField(unique=True, blank=True)
    levels_played = models.ManyToManyField(Level, related_name="player_of_this_level")
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        This method populates slug on first save.
        :param args:
        :param kwargs:
        :return:
        """
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        return super(Player, self).save(*args, **kwargs)

    def get_name(self):
        return self.name

    def update_score(self):
        """
        Run every time a player gets to a new level.
        Also returns the score for ease.
        :return:
        """
        self.score = sum([level.points for level in self.levels_played.all()])
        return self.score

    def get_score(self):
        return self.score


