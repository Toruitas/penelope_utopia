from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from martor.models import MartorField


class GameObject(models.Model):
    """
    A GameObject is something that the player encounters within a Level.
    Players' scores will be determined by what they choose within each level and which GameObjects are within.
    """

    name = models.CharField(max_length=96)
    slug = models.SlugField(unique=True, blank=True)
    variety = models.CharField(
        choices=[
            ('UN', "Unseen"),
            ("P", "Poop"),
            ("A", "Advertisement"),
            ("E", "Emergency"),
            ("B", "Branding"),
            ("L", "Life")
        ],
        max_length=2
    )
    points = models.IntegerField()  # how many points this object is worth

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
        return super(GameObject, self).save(*args, **kwargs)

    def get_name(self):
        return self.name

    def get_slug(self):
        return self.name

    def get_points(self):
        return self.points

    def get_variety(self):
        """
        https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.get_FOO_display
        :return:
        """
        return self.get_variety_display()


class Level(models.Model):
    """
    A level is equivalent to a scene. It contains GameObjects. The whole "game" is made up of a series of Level.

    """
    name = models.CharField(max_length=96)
    slug = models.SlugField(unique=True, blank=True)
    game_objects = models.ManyToManyField(GameObject, blank=True)
    next_levels = models.ManyToManyField("self", symmetrical=False, blank=True)
    description = MartorField()
    button_text = models.CharField(max_length=60)  # this goes on the buttons for when this is a next level
    img_src = models.CharField(max_length=64, blank=True)
    sidebar = models.BooleanField(default=False)
    img_attribution = models.CharField(max_length=96, blank=True)

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
        return super(Level, self).save(*args, **kwargs)

    def get_name(self):
        return self.name

    def get_slug(self):
        return self.slug

    def get_next_levels(self):
        return self.next_levels

    def get_next_button_text(self):
        return [level.get_button_txt() for level in self.next_levels.all()]

    def get_next_slugs(self):
        return [level.get_slug() for level in self.next_levels.all()]

    def get_next_urls(self):
        return [reverse('level', kwargs={"level_slug": level.get_slug()}) for level in self.next_levels.all()]

    def get_next_buttons(self):
        return list(zip(self.get_next_button_text(), self.get_next_urls()))

    def get_description(self):
        return self.description

    def get_game_objects(self):
        return self.game_objects

    def get_points(self):
        """
        We don't save this on the instance, as we want to be pretty dynamic with encounters.
        This way we just re-calculate it each time a player needs it recalculated.
        :return:
        """
        if len(self.game_objects.all()) > 0:
            return sum([game_object.get_points() for game_object in self.game_objects.all()])
        else:
            return 0

    def get_img_src(self):
        return self.img_src

    def get_button_txt(self):
        return self.button_text

    def has_next(self):
        return len(self.next_levels.all())

    def get_attribution(self):
        return self.img_attribution

    def get_sidebar_status(self):
        return self.sidebar


# Create your models here.
class Player(models.Model):
    """
    This Player tracks the player's progress through the game.
    """
    name = models.CharField(max_length=96)
    slug = models.SlugField(unique=True, blank=True)
    levels_played = models.ManyToManyField(Level, related_name="player_of_this_level")
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

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
        self.score = sum([level.get_points() for level in self.levels_played.all()])
        self.save()
        return self.score

    def get_score(self):
        return self.score

    def set_completed(self):
        self.completed = True
        self.save()

    def get_completed(self):
        return self.completed

    def prepare_sidebar_data(self):
        """
        Prepare a data dict. Top level is which variety of object they've encountered.
        :return:
        """
        varieties_dict = {}
        for level in self.levels_played.all():
            for game_obj in level.game_objects.all():
                if game_obj.get_variety() in varieties_dict:
                    varieties_dict[game_obj.get_variety()]["encountered"] += 1
                    varieties_dict[game_obj.get_variety()]["points"] += game_obj.get_points()
                else:
                    varieties_dict[game_obj.get_variety()] = {
                        "encountered": 1,
                        "points": game_obj.get_points()
                    }
        data_dict = {
            "levels_played": len(self.levels_played.all()),
            "varieties": varieties_dict
        }
        print(data_dict)

        return data_dict
