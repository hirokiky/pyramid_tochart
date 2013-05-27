from pyramid.interfaces import IRequest
import venusian
from zope.component.factory import Factory
from zope.component.interfaces import IFactory

from .interfaces import ILinechart
from .linechart import Linechart


def tochart_config(name='', chart_type='linechart'):
    def dec(callable):
        def callback(scanner, _name, ob):
            scanner.config.set_tochart(callable, name, chart_type)
        venusian.attach(callable, callback)
        return callable
    return dec


def set_tochart(config, callable, name="", chart_type='linechart'):
    chart_interface = config.registry.getUtility(IFactory, chart_type).getInterfaces()
    callable = config.maybe_dotted(callable)
    reg = config.registry

    def register():
        reg.registerAdapter(callable,
                            [IRequest, list],
                            chart_interface,
                            name=name)
    intr = config.introspectable(category_name='tochart',
                                 discriminator='tochart of {0}'.format(type.__name__),
                                 title='tochart of {0}'.format(type.__name__),
                                 type_name=None)
    config.action('tochart', register,
                  introspectables=(intr,))


def tochart(request, value, name=''):
    adapted = request.registry.getMultiAdapter([request, value],
                                               ILinechart,
                                               name=name)
    chart = Linechart(adapted)
    return chart


def includeme(config):
    config.add_directive('set_tochart',
                         set_tochart)
    factory = Factory(Linechart, 'Linechart')
    config.registry.registerUtility(factory, IFactory, 'linechart')
