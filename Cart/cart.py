class Cart():
    def __init__(self,request):
        self.session = request.session
        #! get the current session key if it exists
        self.request = request
        cart=self.session.get("session_key")
        
        #! if the  useris new ,no session key, create one
        
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
            
        
        #! make sure cart is available on all pages of site
        self.cart=cart
    
    def add(self, product, quantity):
            product_id = str(product.id)
            product_qty = str(quantity)
            # Logic
            if product_id in self.cart:
                pass
            else:
                #self.cart[product_id] = {'price': str(product.price)}
                self.cart[product_id] = int(product_qty)

            self.session.modified = True