from django.db import models

from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import (
    post_save,
    pre_save,
    pre_delete,
    post_delete,
    m2m_changed,
)
from django.utils import timezone
User = settings.AUTH_USER_MODEL


@receiver(pre_save, sender=User)
def user_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    Before saved in the database
    """
    print(instance.username, instance.id)  # None

    # trigger pre_save
    # Avoid this instance.save()
    # Causes a maximum recurtion error
    # trigger post_save
# pre_save.connect(user_created_handler,sender=User)


@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    After saved in the database
    """
    if created:
        print("Send email to", instance.username)
        # trigger pre_save
        # instance.save()
        # trigger post_save
    else:
        print(instance.username, "was just saved")

# post_save.connect(user_created_handler,sender=User)


class BlogPost(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    liked = models.ManyToManyField(User, blank=True)
    notify_users = models.BooleanField(default=False)
    notify_users_timestamp = models.DateTimeField(
        blank=True, null=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=BlogPost)
def blog_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver(post_save, sender=BlogPost)
def blog_post_save(sender, instance, created, *args, **kwargs):
    if instance.notify_users:
        print("notify users")
        instance.notify_users = False
        # celery worker task
        instance.notify_users_timestamp = timezone.now()
        instance.save()

# Deleting...


@receiver(pre_delete, sender=BlogPost)
def blog_pre_delete(sender, instance, *args, **kwargs):
    # Move or make a backup of this data
    print(f"{instance.id} will be removed.")


@receiver(post_delete, sender=BlogPost)
def blog_post_delete(sender, instance, created, *args, **kwargs):
    print(f"{instance.id} has been removed.")

# Many to Many changed
