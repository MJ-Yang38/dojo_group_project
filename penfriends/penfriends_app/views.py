
from django.shortcuts import render
from .models import Resident,Message,Post
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from login_registration_app.models import User
import bcrypt

# Seeking Penfriends Page (Home)
def penfriends(request): #GET REQUEST
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id=request.session["user_id"])
        if this_user.recipient_messages:
            unread_messages = this_user.recipient_messages.filter(unread = True)
            unread_message_count = unread_messages.count()
        all_the_posts = Post.objects.all()
        context = {
        "this_user": this_user,
        "all_the_posts": all_the_posts,
        "unread_message_count": unread_message_count
    }
    return render(request, "penfriends.html", context)

def become_penfriend(request): #POST REQUEST
    if request.method != "POST":
        return redirect("/")
    elif request.method == "POST":
        this_user = User.objects.get(id = request.session["user_id"])
        this_resident = Resident.objects.get(id = request.POST["resident_id"])
        this_user.penpal_residents.add(this_resident)
        Message.objects.create(subject = "New PenFriend Added", content = this_user.first_name + " " + this_user.last_name + " has added "+ this_resident.first_name + " " + this_resident.last_name + " as a Penfriend", creator = this_user, recipient = this_resident.creator, pen_resident = this_resident)
        messages.success(request, "You added a PenFriend")
    return redirect("/penfriends/dashboard/penpal")

# Admin Dashboard Page
def admindash(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session["user_id"])
        if this_user.recipient_messages:
            unread_messages = this_user.recipient_messages.filter(unread = True)
            unread_message_count = unread_messages.count()
        context = {
            "this_user": this_user,
            "unread_message_count": unread_message_count
        }
        return render(request,'admindash.html', context)

def createresident(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session['user_id'])
        if request.method == "POST" and this_user.category == "admin":
            Resident.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                picture = request.FILES['picture'],
                bio = request.POST['bio'],
                creator = this_user
                )
        return redirect(f'/penfriends/dashboard/admin')

def createpost(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session['user_id'])
        recipient = Resident.objects.get(id = request.POST['for_resident'])
        if request.method =="POST" and this_user.category == "admin":  
            Post.objects.create(
                title = request.POST['title'],
                body = request.POST['body'],
                maker = this_user,
                for_resident = recipient
            )
        return redirect(f'/penfriends/dashboard/admin')

def updatepost(request, post_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        update_post = Post.objects.get(id = post_id)
        if request.method == "POST":
            update_post.title = request.POST['title']
            update_post.body = request.POST['body']
            update_post.save()
        messages.success(request, "Post updated successfully!")
        return redirect(f'/penfriends/dashboard/admin')

def deletepost(request, post_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        if request.method == "POST":
            this_post = Post.objects.get(id = post_id)
            this_post.delete()
            return redirect(f'/penfriends/dashboard/admin')

# Penpal Dashboard Page
def penpal_dash(request): #GET REQUEST
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session["user_id"])
        if this_user.recipient_messages:
            unread_messages = this_user.recipient_messages.filter(unread = True)
            unread_message_count = unread_messages.count()
        if this_user.category != "penpal":
            messages.error(request, "You are not authorized to view this page")
            return redirect ("/")
        else:
            all_the_residents = this_user.penpal_residents.all()
            context = {
                "this_user": this_user,
                "all_the_residents": all_the_residents,
                "unread_message_count": unread_message_count
            }
            return render(request, "penpal_dash.html", context)

def update_penpal_password(request): #POST REQUEST
    if request.method != "POST":
        return redirect("/")
    elif request.method == "POST":
        this_user = User.objects.get(id = request.session["user_id"])
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        this_user.password = pw_hash
        this_user.save()
        messages.success(request, "Password updated")
    return redirect("/penfriends/dashboard/penpal")

def remove_penpal(request): #POST Request
    if request.method != "POST":
        return redirect("/")
    this_resident = Resident.objects.get(id = request.POST["resident_id"])
    this_user = User.objects.get(id = request.session["user_id"])
    if request.method == "POST":
        this_user.penpal_residents.remove(this_resident)        
        messages.success(request, "PenFriend removed")
    return redirect("/penfriends/dashboard/penpal")

# Resident Profile Page
def residentprofile(request, resident_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session["user_id"])
        this_resident = Resident.objects.get(id = resident_id)
        if this_user.recipient_messages:
            unread_messages = this_user.recipient_messages.filter(unread = True)
            unread_message_count = unread_messages.count()
        context = {
            "this_resident": this_resident,
            "this_user": this_user,
            "unread_message_count": unread_message_count,
        }
        return render(request, "residentprofile.html", context)

def updateresident(request, resident_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        update_resident = Resident.objects.get(id = resident_id)
        if request.method == "POST":
            update_resident.first_name = request.POST['first_name']
            update_resident.last_name = request.POST['last_name']
            update_resident.bio = request.POST['bio']
            update_resident.picture = request.FILES['picture']
            update_resident.save()
        messages.success(request, "Resident info updated successfully!")
        return redirect(f'/penfriends/resident/{resident_id}')   

def deleteresident(request, resident_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        if request.method == "POST":
            this_resident = Resident.objects.get(id = resident_id)
            this_resident.delete()
            return redirect(f'/penfriends/dashboard/admin')

# Inbox Page
def inbox(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session["user_id"])
        if this_user.recipient_messages:
            unread_messages = this_user.recipient_messages.filter(unread = True)
            unread_message_count = unread_messages.count()
        context = {
            "this_user": this_user,
            "user_messages": Message.objects.filter(recipient = this_user).order_by("-created_at"),
            "unread_message_count": unread_message_count
        }
        return render (request, "inbox.html", context)

def mark_read(request):
    this_message = Message.objects.get(id = request.POST["message_id"])
    this_message.unread = False
    this_message.save()
    return redirect("/penfriends/inbox")

def mark_unread(request):
    this_message = Message.objects.get(id = request.POST["message_id"])
    this_message.unread = True
    this_message.save()
    return redirect("/penfriends/inbox")

def delete_message(request): 
    this_message = Message.objects.get(id = request.POST["message_id"])
    this_message.delete()
    return redirect("/penfriends/inbox")

# Create Message Page
def new_message(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user=User.objects.get(id = request.session['user_id'])
        if this_user.recipient_messages:
            unread_messages = this_user.recipient_messages.filter(unread = True)
            unread_message_count = unread_messages.count()
        if this_user.category=="admin":
            all_recipients = User.objects.filter(category="penpal")
        else:
            all_recipients = User.objects.filter(category="admin")
        context = {
            "this_user": this_user,
            "all_recipients": all_recipients,
            "unread_message_count": unread_message_count
        }
        return render(request, "newmsg.html", context)

def create_message(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session['user_id'])
        recipient = User.objects.get(id = request.POST["recipient_id"])
        pen_resident = Resident.objects.get(id = request.POST["resident_id"])
        if request.method == "POST":
            create = Message.objects.create(
                subject = request.POST['subject'],
                content = request.POST['content'],
                attachment = request.FILES['attachment'],
                creator = this_user,
                recipient = recipient,
                pen_resident = pen_resident,
            )
            message_id = create.id
            return redirect(f'/penfriends/message/{message_id}')

# View Message Page
def message(request, message_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = User.objects.get(id = request.session["user_id"])
        this_message = Message.objects.get(id = message_id)
        if this_user.recipient_messages:
            unread_messages = this_user.recipient_messages.filter(unread = True)
            unread_message_count = unread_messages.count()
        context = { 
            "this_user": this_user,
            "message": this_message,
            "unread_message_count": unread_message_count,
        }
        return render (request, "message.html", context)