import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','first_project.settings')

import django
django.setup()

## FAKE POP SCRIPTS
import random
from first_app.models import users
from faker import Faker

fakegen = Faker('en_TH')
# topic = ['Search','Social','Marketplace','News','Games']

# def add_topic():
#     t = Topic.objects.get_or_create(top_name=random.choice(topic))[0]
#     t.save()
#     return t

def populate(N=5):

    for entry in range(N):

        fake_first_name = fakegen.first_name()
        fake_last_name = fakegen.last_name()
        fake_email = fakegen.email()

        # New entry
        user = users.objects.get_or_create(first_name=fake_first_name,last_name=fake_last_name, email=fake_email)[0]

if __name__ == '__main__':
    print("populating database!")
    populate(20)
    print("populating complete!")
