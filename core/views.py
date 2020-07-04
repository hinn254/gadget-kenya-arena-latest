from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from core.models import Item, Order, OrderItem, BillingAddress
from django.db.models import Q
from core.forms import CheckOutForm
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, View,TemplateView



class SearchResultsVIew(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
            )
        return object_list


class OrderSubmitedView(LoginRequiredMixin,TemplateView):
    model = Order
    template_name = 'core/order_snippet_page.html'


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        #form
        form = CheckOutForm()
        context = {
            'form':form,
            'order':order
            }
        return render(self.request, 'core/checkout.html', context)


    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email_address = form.cleaned_data.get('email_address')
                phone_number = form.cleaned_data.get('phone_number')
                country = form.cleaned_data.get('country')
                address = form.cleaned_data.get('address')
                # TODO: add functionality
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user = self.request.user,
                    first_name = first_name,
                    last_name = last_name,
                    email_address = email_address,
                    phone_number = phone_number,
                    country = country,
                    address = address,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                order_items = order.items.all()
                order_items.update(ordered=True)

                for item in order_items:
                    item.save()

                order.ordered = True
                order.save()
                # TODO: add redirect to the selected payment option
                messages.success(self.request, "Your order was successful!")
                return redirect('core:order-submitted')
                          
            messages.warning(self.request, 'Invalid entries. Please fill the form correctly')
            return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request,'You do not have an active order')
            return redirect('core:order-summary') 
        print(self.request.POST)


class HomeView(ListView):
    model = Item    
    template_name = 'core/home-page-one.html'
     

class OrderSummaryView(View):  
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)


            context ={
                'object':order
            }
            return render(self.request, 'core/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request,'You do not have an active order')
            return redirect('/') 


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product-page.html'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered=False
        
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is int the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,'This item quantity was updated')
            return redirect('core:order-summary')

        else:
            messages.info(request,'This item was added to your cart')
            order.items.add(order_item)
            return redirect('core:order-summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,'This item was added to your cart')
        return redirect('core:order-summary')

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is int the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered=False
        
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request,'This item was removed from your cart')
            return redirect('core:order-summary')
        else:

            # add a message saying the order doesnt contain the item
            messages.info(request,'This item was not in your cart')
            return redirect('core:product', slug=slug) 

    else:
        # add a message saying the user doesnt have an order
        messages.info(request,'You do not have an active order')

        return redirect('core:product', slug=slug)

    
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is int the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered=False
        
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect('core:order-summary')
        else:

            # add a message saying the order doesnt contain the item
            messages.info(request,'This item was not in your cart')
            return redirect('core:product', slug=slug) 

    else:
        # add a message saying the user doesnt have an order
        messages.info(request,'You do not have an active order')

        return redirect('core:product', slug=slug)



class SearchResultsAcc(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(description__icontains='Accessories') | Q(description__icontains='Accessory') | Q(description__icontains='accessories') | Q(description__icontains='accessor') | Q(description__icontains='Accessor')
            )
        return object_list

class SearchResultsIphone(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='IPHONE') | Q(title__icontains='iPhone') | Q(title__icontains='iphone') 
            )
        return object_list

class SearchResultsOppo(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='OPPO') | Q(title__icontains='Oppo') | Q(title__icontains='oppo') 
            )
        return object_list

class SearchResultsNokia(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='NOKIA') | Q(title__icontains='Nokia') | Q(title__icontains='nokia') 
            )
        return object_list

class SearchResultsHuawei(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='HUAWEI') | Q(title__icontains='Huawei') | Q(title__icontains='huawei') 
            )
        return object_list

class SearchResultsSamsung(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='SAMSUNG') | Q(title__icontains='Samsung') | Q(title__icontains='samsung') 
            )
        return object_list

class SearchResultsTecno(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='TECNO') | Q(title__icontains='Tecno') | Q(title__icontains='tecno') 
            )
        return object_list

class SearchResultsRedmi(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='redmi') | Q(title__icontains='REDMI') | Q(title__icontains='Redmi') 
            )
        return object_list

class SearchResultsInfinix(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='Infinix') | Q(title__icontains='infinix') | Q(title__icontains='INFINIX') 
            )
        return object_list

class SearchResultsHtc(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='HTC') | Q(title__icontains='Htc') | Q(title__icontains='htc') 
            )
        return object_list

class SearchResultsRealMe(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='REALME') | Q(title__icontains='realme') | Q(title__icontains='Realme') 
            )
        return object_list

class SearchResultsOneplus(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='oneplus') | Q(title__icontains='Oneplus') | Q(title__icontains='ONEPLUS') 
            )
        return object_list

class SearchResultsHot(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.order_by('discount_price')
        return object_list


class SearchResultsTablet(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='tablet') | Q(title__icontains='TABLET') | Q(title__icontains='Tablets') 
            )
        return object_list


class SearchResultsComputer(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='computer') | Q(title__icontains='laptop') | Q(title__icontains='LAPTOP') 
            )
        return object_list


class SearchResultsVivo(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='VIVO') | Q(title__icontains='vivo') | Q(title__icontains='Vivo') 
            )
        return object_list


class SearchResultsLaptop(ListView):
    model = Item
    paginate_by = 16
    template_name = 'core/search_results.html'

    def get_queryset(self):
        object_list = Item.objects.filter(
            Q(title__icontains='laptop') | Q(title__icontains='Laptop') | Q(title__icontains='LAPTOP') 
            )
        return object_list