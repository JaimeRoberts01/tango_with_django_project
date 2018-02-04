from django.db import models
from django.template.defaultfilters import slugify # Added 23.01.2018
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model): # Added by JNR 22.01.2018
    name = models.CharField (max_length=128, unique=True)
    views = models.IntegerField (default=0) # Added by JNR 22.01.2018
    likes = models.IntegerField (default=0) # Added by JNR 22.01.2018
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs): # Added by JNR 23.01.2018
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta: # Added by JNR 22.01.2018
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Page(models.Model): # Added by JNR 22.01.2018
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model): # Added by JNR 23.01.2018
    # This line is required as it links Userprofile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!

    def __str__(self):
        return self.user.username