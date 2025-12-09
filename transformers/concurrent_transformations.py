import random


@transformer
def transform(data, *args, **kwargs):
    return (data['uuid'] + 1) * random.randint(1, 100)