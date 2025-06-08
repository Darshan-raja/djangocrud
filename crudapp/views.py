from django.shortcuts import render 
from django.shortcuts import get_object_or_404

from .models import Student
from django.contrib import messages
from django.db.models import Q


# Create your views here.

def index(request):
    students = Student.objects.all() #  Get all students from the database
    query = ""
    if request.method=="POST": #  Check if the request method is POST
       if  "add" in request.POST: #  Check if the "add" button was clicked
           name = request.POST.get("name") #  Get the name and email from the form
           email = request.POST.get("email")
           Student.objects.create( #  Create a new student object and save it to the database
               name=name,
               email=email           
           )
           messages.success(request, "Student Added Successfully")
           
       elif "update" in request.POST: #  Check if the request method is POST and if the "update" key is in the POST data
           id = request.POST.get("id") #  Get the id, name, and email from the POST data
           name = request.POST.get("name") #  Get the name from the POST request
           email = request.POST.get("email") #  Get the email from the POST request
           
           update_student = Student.objects.get(id=id) #  Get the student object with the given id
           update_student.name = name #  Update the name and email of the student object
           update_student.email = email
           update_student.save() #  Save the updated student object
           
           messages.success(request, "Student Updated Successfully")  #  If the request method is POST and the key "update" is in the request.POST dictionary
           
       elif "delete" in request.POST: #  If the request method is POST and the key "delete" is in the request.POST dictionary
        id = request.POST.get("id") #  Get the id from the request.POST dictionary
        Student.objects.get(id=id).delete() #  Delete the student with the given id
        messages.success(request, "Student Deleted Successfully") #  Display a success message
        
       elif "search" in request.POST: #  If the request method is POST and the key "search" is in the request.POST dictionary
           query = request.POST.get("query")
           students = Student.objects.filter(Q(name__icontains=query) | Q(email__icontains=query)) 
           
           
    

    context = {"students": students, "query": query} #  Create a context dictionary with the students and query
    return render(request, 'index.html', context=context)  #  Render the index.html template with the context
