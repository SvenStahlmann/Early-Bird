from .models import Instance
def get_instances():
    instances = {}

    for instance in Instance.objects.all():
        instances[instance] = list(instance.Encounter.all())

    return instances