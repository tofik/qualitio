from mptt.models import MPTTModel
from django.core.exceptions import ObjectDoesNotExist
from qualitio.core.utils import json_response


def to_tree_element(object, type):
    tree_element = {'attr': {'id': "%s_%s" % (object.pk, type),
                             'rel': type},
                    'data': object.name}

    if isinstance(object, MPTTModel):
        try:
            subchildren = getattr(getattr(object, "subchildren", None), "all", None)()
        except TypeError:  # Not really good idea, slow typecheck?
            subchildren = None
        if object.get_children() or subchildren:
            tree_element['state'] = "closed"

    return tree_element


@json_response
def get_children(request, directory):
    data = []

    try:
        node_id = int(request.GET.get('id', 0))
        node = directory.objects.get(pk=node_id)
        directories = node.children.all()
        data = map(lambda x: to_tree_element(x, x._meta.module_name), directories)
        try:
            subchildren = getattr(getattr(node, "subchildren", None), "all", None)()
            data.append(map(lambda x: to_tree_element(x, x._meta.module_name), subchildren))
        except TypeError:  # Not really good idea, slow typecheck?
            pass

    except (ObjectDoesNotExist, ValueError):
        # TODO: maybe the better way is to override method 'root_nodes' on manager
        directories = directory.tree.root_nodes().order_by('name')
        data = map(lambda x: to_tree_element(x, x._meta.module_name),
                   directories)

    return data
