from .models import Instance


def get_instances():
    instances = {}

    for instance in Instance.objects.all():
        instances[instance] = list(instance.encounter.all())

    return instances