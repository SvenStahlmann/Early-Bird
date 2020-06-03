from .models import WowClass


def get_classes():
    classes = {}

    for wowclass in WowClass.objects.all():
        classes[wowclass] = list(wowclass.specialization.all())

    return classes
