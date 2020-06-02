from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    email = models.EmailField(help_text='E-Mail des Benutzers.')

    # One to one
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='One-to-one Beziehung zu django User.')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class WowClass(models.Model):
    name = models.CharField(max_length=80, help_text='Name der Klasse.')
    icon = models.ImageField(upload_to='class_icons/', help_text='Icon der Klasse.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=80, help_text='Name der Spezialisierung.')
    icon = models.ImageField(upload_to='specialization_icons/', help_text='Icon der Spezialisierung.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Foreign key
    wow_class = models.ForeignKey(WowClass, related_name='specialization', on_delete=models.CASCADE)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.wow_class) + ' - ' + self.name


class Character(models.Model):
    name = models.CharField(max_length=80, help_text='Name des Charakters.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Foreign keys
    user = models.ForeignKey(User, related_name='character', on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, related_name='character', on_delete=models.CASCADE)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
