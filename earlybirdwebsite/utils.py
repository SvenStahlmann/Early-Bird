from raids.models import Instance


def get_instances():
    instances = {}

    for instance in Instance.objects.all():
        instances[instance] = list(instance.encounter.all())

    return instances


def is_integer(value: str, *, base: int = 10) -> bool:
    try:
        int(value, base=base)
        return True
    except ValueError:
        return False
