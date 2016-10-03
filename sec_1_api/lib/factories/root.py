from pyramid.security import Allow, Everyone


class RootFactory(dict):

    def __init__(self, request):
        self.request = request
        self.__name__ = None
        self.__parent__ = None

    def __acl__(self):
        return ((Allow, Everyone, 'public'),)
