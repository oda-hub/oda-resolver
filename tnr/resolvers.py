import importlib
import pkgutil
import inspect

import tnr.plugins

class Resolver:
    def resolve(self,name):
        pass


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


class ResolverToPlugins(Resolver):
    def __init__(self):
        self.discover_plugins()

    def discover_plugins(self):
        self.resolver_plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in iter_namespace(tnr.plugins)
        }
        print("discovered plugin modules: "+", ".join(self.resolver_plugins))

        self.resolvers=dict()

        for plugin_name, plugin in self.resolver_plugins.items():
            module_resolvers=dict()
            for name, cls in plugin.__dict__.items():
                if inspect.isclass(cls) and issubclass(cls,Resolver) and cls != Resolver:
                    module_resolvers[plugin_name.replace("tnr.plugins.","")+"."+name]=cls

            print("discovered resolver in module: "+", ".join(module_resolvers))
            self.resolvers.update(module_resolvers)

    def resolve(self,name):
        return {
            plugin_name: plugin().resolve(name)
            for plugin_name, plugin in self.resolvers.items()
        }
            

RootResolver=ResolverToPlugins

