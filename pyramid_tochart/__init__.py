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
    chart_interface = list(config.registry.getUtility(IFactory, chart_type).getInterfaces())[0]
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


def add_chart_factory(config, chart_type, factory_class):
    factory = Factory(factory_class)
    config.registry.registerUtility(factory, IFactory, chart_type)


def tochart(request, value, name='', chart_type='linechart'):
    chart_factory = request.registry.getUtility(IFactory, chart_type)
    chart_interface = list(chart_factory.getInterfaces())[0]

    adapted = request.registry.getMultiAdapter([request, value],
                                               chart_interface,
                                               name=name)
    chart = chart_factory(adapted)
    return chart


def includeme(config):
    config.add_directive('set_tochart',
                         set_tochart)
    config.add_directive('add_chart_factory',
                         add_chart_factory)

    config.add_chart_factory('linechart', Linechart)
