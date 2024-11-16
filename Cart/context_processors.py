from .cart import Cart

#!carte context processor so out cart can work on all pages

def cart(request):
    #! return the default data fromm our cart
    return {'cart':Cart(request)}
