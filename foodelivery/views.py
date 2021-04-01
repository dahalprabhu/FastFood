from django.shortcuts import render,redirect ,get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from .models import FoodItems, Resturants ,Order , OrderItem ,ShippingAddress, Customer
from django.views.generic import ListView, DetailView 
from django.utils import timezone

from django.http import HttpResponse

from django.db.models import Q

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

def Restaurants(request):
    restaurant= Resturants.objects.all()
    foods= FoodItems.objects.all()

    return render(request, 'index.html',{'res':restaurant, 'foods':foods})



class ResturantDetailView(DetailView):
    model= Resturants
    template_name= "resturant.html"
    
    def get_context_data(self, **kwargs):
        context=super(ResturantDetailView, self).get_context_data(**kwargs)
        print(self)
        context['fooditems']=FoodItems.objects.filter(resturant = self.object)
        return context

def add_to_cart(request, slug):
    if request.user.is_authenticated:
        print('uuuuuuuuuuuuu in add to cart', slug)

        item= get_object_or_404(FoodItems, slug=slug)
        
        order_item, created= OrderItem.objects.get_or_create(item=item,
            user=request.user, is_ordered=False)
        print('mmmmmmmmmmmmmmmmmmmmmmmmm',order_item)
        order_qs= Order.objects.filter(user= request.user, is_ordered= False)
    
        if order_qs.exists():
            order=order_qs[0]
            print('order_qs', order_qs)
            print('order_qs[0]', order_qs[0])

            #check if the orderitem is in the order
            if order.items.filter(item__slug=item.slug).exists(): 
                order_item.quantity +=1
                order_item.save()
            else:
                order.items.add(order_item)
        else: 
            order=Order.objects.create(user=request.user) 
            order.items.add(order_item)  
        
    else:
         messages.info(request, 'You have to login to add items to cart')
         
    return redirect("/")   
    


def remove_from_cart(request, pk):
    print("sssssssssssssssssssss", pk)
    item= get_object_or_404(OrderItem, pk=pk)
    print('ddddddddddddddddddddd', item)
    order_qs=Order.objects.filter(user=request.user, is_ordered= False)
    if order_qs.exists():
        order=order_qs[0]
        order.items.remove(item)
    return redirect('/cart/')



@login_required(login_url='login')
def Cart(request):
    if request.user.is_authenticated:
        order_qs= Order.objects.filter( user=request.user, is_ordered=False)
        if order_qs.exists():
            order=order_qs[0]      
            cartitems= order.items.all()
            totalling=0       
            for i in cartitems:
                totalling = totalling + i.get_total_price()
            return render (request, 'cart.html', {'cartitems':cartitems, 'totalling':totalling})    

        return render(request, 'cart.html' )
    else:
        messages.info(request, 'You have to login to see your cart')
        return redirect('/')
def Checkout(request):
    if request.method == 'POST':

        address= request.POST['address']
        datetime= request.POST['datetime']
        phoneno=request.POST['phone-number']
        order = Order.objects.get(user=request.user, is_ordered=False)
        
        checkouting= ShippingAddress.objects.create(address=address, datetime=datetime, user=request.user, order=order, phoneno=phoneno)
        checkouting.save()
        #
        order.is_ordered= True
        order.save()
       
        print("shipping adress added ")
        return redirect('/feedback/')
    else:
        order_qs= Order.objects.filter( user=request.user, is_ordered=False)
        if order_qs.exists():
            order=order_qs[0]      
            cartitems= order.items.all()
            totalling=0       
            for i in cartitems:
                totalling = totalling + i.get_total_price()
        return render(request, 'fullcheckout.html',{'cartitems':cartitems, 'totalling':totalling})
def feedback(request):
    return render(request, 'feedback.html')







def add_singleitem_to_cart(request, slug):

    print('uuuuuuuuuuuuu in add to cart', slug)

    item= get_object_or_404(FoodItems, slug=slug)
    
    order_item, created= OrderItem.objects.get_or_create(item=item,
        user=request.user, is_ordered=False)
    order_qs= Order.objects.filter(user= request.user, is_ordered= False)
   
    if order_qs.exists():
        order=order_qs[0]
        print('order_qs', order_qs)
        print('order_qs[0]', order_qs[0])

        #check if the orderitem is in the order
        if order.items.filter(item__slug=item.slug).exists(): 
            order_item.quantity +=1
            order_item.save()
        else:
            order.items.add(order_item)
    else: 
        order=Order.objects.create(user=request.user) 
        order.items.add(order_item)   
    return redirect("/cart/")

def remove_singleitem_to_cart(request, slug):

    print('uuuuuuuuuuuuu in add to cart', slug)

    item= get_object_or_404(FoodItems, slug=slug)
    order_item= OrderItem.objects.get(item=item, user=request.user, is_ordered=False)

    order_qs= Order.objects.filter(user=request.user, is_ordered=False)
    
    if order_qs.exists():
        order=order_qs[0]
        if order_item.quantity > 1:
            order.items.filter(item__slug=item.slug)
            order_item.quantity -= 1
            order_item.save()
        else:
            order.items.remove(order_item)
    return redirect('/cart/')

########################################################################################

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('/login')
		

	context = {'form':form}
	return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('/')


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['owner'])
# def dashboard(request):
#     #item= get_object_or_404(Resturants, slug)
#     order_false= Order.objects.filter(is_ordered=False)
#     incartotal= order_false.count()
#     order_qs= Order.objects.filter(is_ordered=True)
#     if order_qs.exists:
#         order= order_qs[0]
#         print('lsllsldklldklfkjkfkjkfkldskldfdkfkljkl', order)
#         order_item= order.items.all()
#         sum=0
#         foodsarray=[]
#         for i in order_item:
#             if i.item.resturant.name == 'Dahal Vandar':
#                 i
#                 sum= sum+1
#                 foodsarray.append(i)
#                 print('looooooooooooooooooooooooooooooooooooooooooooo', i)
#             print('hhhhhhhhhhhhhhhhhhhhh',i.item.resturant)
#         print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', foodsarray)
    
#     return render(request, 'dashboard.html', {'foodsarray':foodsarray ,'sum':sum, 'incartotal':incartotal})


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def dashboard(request):
    #item= get_object_or_404(Resturants, slug)
    order_false= Order.objects.filter(is_ordered=False)
    incartotal= order_false.count()
    order_qs= Order.objects.filter(is_ordered=True)
    sum=0
    foodsarray=[]
    if order_qs.exists():
        print('........................................', order_qs)
        for i in order_qs:
            order_item= i.items.all()
            for j in order_item:
                if j.item.resturant.name == 'Dahal Vandar':
                    sum= sum+1
                    foodsarray.append(j)
                    print('looooooooooooooooooooooooooooooooooooooooooooo', j)
            print('hhhhhhhhhhhhhhhhhhhhh',j.item.resturant)
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', foodsarray)

    return render(request, 'dashboard.html', {'foodsarray':foodsarray ,'sum':sum, 'incartotal':incartotal})

@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def dashboardblue(request):
    #item= get_object_or_404(Resturants, slug)
    order_false= Order.objects.filter(is_ordered=False)
    incartotal= order_false.count()
    order_qs= Order.objects.filter(is_ordered=True)
    sum=0
    foodsarray=[]
    if order_qs.exists():
        print('........................................', order_qs)
        for i in order_qs:
            order_item= i.items.all()
            for j in order_item:
                if j.item.resturant.name == 'Blue Lagoon':
                    sum= sum+1
                    foodsarray.append(j)
                    print('looooooooooooooooooooooooooooooooooooooooooooo', j)
            print('hhhhhhhhhhhhhhhhhhhhh',j.item.resturant)
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', foodsarray)

    return render(request, 'dashboard2.html', {'foodsarray':foodsarray ,'sum':sum, 'incartotal':incartotal})

@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def dashboardbajeko(request):
    #item= get_object_or_404(Resturants, slug)
    order_false= Order.objects.filter(is_ordered=False)
    incartotal= order_false.count()
    order_qs= Order.objects.filter(is_ordered=True)
    sum=0
    foodsarray=[]
    if order_qs.exists():
        print('........................................', order_qs)
        for i in order_qs:
            order_item= i.items.all()
            for j in order_item:
                if j.item.resturant.name == 'Bajeko Sekuwa':
                    sum= sum+1
                    foodsarray.append(j)
                    print('looooooooooooooooooooooooooooooooooooooooooooo', j)
            print('hhhhhhhhhhhhhhhhhhhhh',j.item.resturant)
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', foodsarray)

    return render(request, 'dashboard3.html', {'foodsarray':foodsarray ,'sum':sum, 'incartotal':incartotal})
#############################################################################################33

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def userPage(request):
	

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()
   

	context = {'form':form}
	return render(request, 'account_settings.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
	order = OrderItem.objects.get(id=pk)
	form = OrderForm(instance=order)
	print('ORDER:', order)
	if request.method == 'POST':

		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = OrderItem.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'delete.html', context)


#####################################3

def search(request):
  if request.method== 'POST':
    srch = request.POST['srh']
    if srch:
     
      match = FoodItems.objects.filter(Q(name__icontains=srch))
      
      if match:
        return render(request,'search.html',{'sr':match})
      else:
                messages.error(request,'no results found')
    else:
        return HttpResponseRedirect('/search')
    
            
    return render(request,'search.html')  