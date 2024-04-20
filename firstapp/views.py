from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Book

# Create your views here.

@login_required
@csrf_exempt
def home(request): 
    # print(request.method)
    if request.method == "POST":
        data = request.POST
        # print(request.POST)
        bid = data.POST.get("book_id")
        name = data.POST.get("book_name")
        qty = data.POST.get("book_qty")
        price = data.POST.get("book_price")
        author = data.POST.get("book_author")
        is_pub= data.POST.get("book_is_pub")
        # print(request.POST)
        # print(name, qty, price, author, is_pub)
        if is_pub == "Yes":
            is_pub = True
        else:
            is_pub = False
        if not bid:
            Book.objects.create(name=name, qty=qty, price=price, author=author, is_published=is_pub)
        else:
            book_obj = Book.objects.get(id=bid)
            book_obj.name = name
            book_obj.qty = qty
            book_obj.price = price
            book_obj.author = author
            book_obj.is_published = is_pub
            book_obj.save()
        
        # return redirect("home_page")
        return HttpResponse("Success")


    elif request.method == "GET":
        # pront(request.GET)
        return render(request, "old_home.html", context={"person_name": "Abhishek"})

@login_required    
def show_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=True), "active": True})

@login_required
def update_book(request, id): 
    book_obj = Book.objects.get(id=id)
    return render(request, "home.html", context={"single_book": book_obj})

@login_required
def delete_book(request, pk): # hard delete
    Book.objects.get(id=pk).delete()
    return redirect("all_active_books")

@login_required
def soft_delete_book(request, pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = False
    book_obj.save()
    return redirect("all_inactive_books")

@login_required
def show_inactive_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=False), "inactive": True})

@login_required
def restore_book(request, pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = True
    book_obj.save()
    return redirect("all_active_books")

from .forms import BookForm, AddressForm
# from django.contrib.auth.forms import UserCreationForm  

@login_required
def book_form(request):
    return render(request, "book_form.html", {"form":BookForm()})


# simpleisbetterthancomplex

def sibtc(request):
    return render(request, "sibtc.html", {"form": AddressForm()})

# from django.views import View 

# class NewView(View):  
#     def get(self, request):  
#         # View logic will place here  
#         return HttpResponse('get response')  
    
#     def post(self, request):  
#         # View logic will place here  
#         return HttpResponse('post response')  
    
#     def put(self, request):    #update 
#         # View logic will place here  
#         return HttpResponse('put response')  
    
#     def patch(self, request):  #partial information update
#         # View logic will place here  
#         return HttpResponse('patch response')  
    
#     def delete(self, request):   #delete
#         # View logic will place here  
#         return HttpResponse('delete response')  


#CRUD
from django.views.generic.edit import CreateView


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = "/cbv-create-book/"



from django.views.generic.list import ListView  
  
class BookRetrieve(ListView):  
    model = Book
    context_object_name = "all_books"
    # queryset = Book.objects.all()


    # def get_queryset(self):
    #     print("in method")
    #     return Book.objects.filter(is_active=1)
    

from django.views.generic.detail import DetailView  
  
class BookDetail(DetailView):  
    model = Book


from django.views.generic.edit import UpdateView 

class BookUpdate(UpdateView):  
    model = Book 
    fields = '__all__'
    success_url = "/cbv-create-book/"

from django.views.generic.edit import DeleteView 

class BookDelete(DeleteView):  
    model = Book 
  
    # here we can specify the URL   
    # to redirect after successful deletion  
    success_url = "/cbv-create-book/"
     

from django.http import HttpResponse
import csv

def create_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="test.csv"'

    writer = csv.writer(response)
    writer.writerow(['name','qty', 'price', 'author', 'is_published', 'is_active'])

    books = Book.objects.all().values_list('name','qty', 'price', 'author', 'is_published', 'is_active')
    for book in books:
        writer.writerow(book)
    return response

def upload_csv(request):
    file = request.FILES["csv_file"]    
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    lst = []
    for element in reader:
        is_pub = element.get("is_publised")
        if is_pub == "TRUE":
            is_pub = True
        else:
            is_pub = False
        lst.append(Book(name=element.get("name"), qty=element.get("qty"), price=element.get("price"), author=element.get("author"), is_published=is_pub))
        # print(reader)
        Book.objects.bulk_create(lst)
        return HttpResponse("Success")

    expected_header_lst = ['name', "qty", "price", "author", "is_published"]
    expected_header_lst.sort()

    actual_header_lst = decoded_file[0].split(",")
    actual_header_lst.sort()
    print(expected_header_lst, actual_header_lst)
    if expected_header_lst != actual_header_lst:
        return HttpResponse("Error...Headers are not equal..!")