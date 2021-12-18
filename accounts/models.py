from django.db import models

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import (
post_save,
pre_save
)
User=settings.AUTH_USER_MODEL
@receiver(pre_save,sender=User) 
def user_pre_save_receiver(sender,instance,*args,**kwargs):
    """
    Before saved in the database
    """
    print(instance.username,instance.id) #None

    #trigger pre_save
    #Avoid this instance.save()
    #Causes a maximum recurtion error
    #trigger post_save
# pre_save.connect(user_created_handler,sender=User)



@receiver(post_save,sender=User)
def user_post_save_receiver(sender,instance,created,*args,**kwargs):
    """
    After saved in the database
    """
    if created:
        print("Send email to",instance.username)
        #trigger pre_save
        # instance.save()
        #trigger post_save
    else:
        print(instance.username,"was just saved")

# post_save.connect(user_created_handler,sender=User)
