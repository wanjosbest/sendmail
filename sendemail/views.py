from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from .models import Audience, Subscriber, EmailTemplate, Campaign, EmailLog,User,NewsletterSubscriber
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
def home(request):
    return render(request, "index.html")
# ---------- AUTH VIEWS ----------

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not username or not email or not password or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "auth/register.html")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "auth/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "auth/register.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful. Please log in.")
        return redirect("login")

    return render(request, "auth/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")  
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "auth/login.html")

    return render(request, "auth/login.html")


@login_required
def logout(request):
    auth_logout(request)
    return redirect("login")


# ---------- DASHBOARD ----------

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# ---------- AUDIENCE VIEWS ----------

@login_required
def audience_list(request):
    audiences = Audience.objects.filter(user=request.user)
    return render(request, "audiences/audience_list.html", {"audiences": audiences})


@login_required
def audience_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        if name:
            Audience.objects.create(user=request.user, name=name, email=email)
            return redirect("audiences")
        else:
            return render(request, "audiences/audience_form.html", {"error": "Name is required."})
    return render(request, "audiences/audience_form.html")
@login_required
def import_contact(request):
    if request.method =="POST" and request.FILES.get("csv_file"):
        tag = request.POST.get("tag")
        csv_file = request.FILES.get("csv_file")
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "please upload csv_file")
            return redirect("import_contact")
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        added, skipped = 0,0
        for row in reader:
            email = row.get("Email")
            name = row.get("Name")

            if email:
                obj, created = Audience.objects.get_or_create(user=request.user, email=email, name=name,tag=tag)

                if created:
                    added  =+1
                else:
                    skipped =+1
                
                messages.success(request, f'{added} contacts added, {skipped} skipped')
                # return redirect('audiences')
    return render(request, "audiences/audience_form_csv.html")

        

@login_required
def audience_update(request, audience_id):
    audience = get_object_or_404(Audience, pk=audience_id, user=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            audience.name = name
            audience.save()
            return redirect("audiences")
        else:
            return render(request, "audiences/audience_form.html", {"audience": audience, "error": "Name is required."})
    return render(request, "audiences/audience_form.html", {"audience": audience})


@login_required
def audience_delete(request, audience_id):
    audience = get_object_or_404(Audience, pk=audience_id, user=request.user)
    if request.method == "POST":
        audience.delete()
        return redirect("audiences")
    return render(request, "audiences/audience_confirm_delete.html", {"audience": audience})


# ---------- SUBSCRIBER VIEWS ----------

@login_required
def subscriber_list(request):
    subscribers = Subscriber.objects.all()
    NewsletterSubs = NewsletterSubscriber.objects.all()
    return render(request, "subscribers/subscriber_list.html", {"subscribers": subscribers, "newssubs":NewsletterSubs})


@login_required
def subscriber_create(request):
    audiences = Audience.objects.filter(user=request.user)
    if request.method == "POST":
        # email = request.POST.get("email")
        # name = request.POST.get("name")
        audience_id = request.POST.get("audience")
        getaud = Audience.objects.get(pk = audience_id)
        email = getaud.email
        name = getaud.name
        if email and audience_id:
            audience = get_object_or_404(Audience, pk=audience_id, user=request.user)
            Subscriber.objects.create(email=email, name=name, audience=audience, subscribed=True)
            return redirect("subscribers")
        else:
            return render(request, "subscribers/subscriber_form.html", {"audiences": audiences, "error": "Email and audience are required."})
    return render(request, "subscribers/subscriber_form.html", {"audiences": audiences})
@login_required
def sub_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        save = NewsletterSubscriber.objects.create(name=name, email=email)
        save.save()
        messages.success(request, "Thanks for Subscribing")
    return render(request, "subscribers/subscriber_newsletter.html")


@login_required
def subscriber_update(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk, audience__user=request.user)
    audiences = Audience.objects.filter(user=request.user)
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        audience_id = request.POST.get("audience")
        if email and audience_id:
            audience = get_object_or_404(Audience, pk=audience_id, user=request.user)
            subscriber.email = email
            subscriber.name = name
            subscriber.audience = audience
            subscriber.save()
            return redirect("subscriber_list")
        else:
            return render(request, "subscribers/subscriber_form.html", {"subscriber": subscriber, "audiences": audiences, "error": "Email and audience are required."})
    return render(request, "subscribers/subscriber_form.html", {"subscriber": subscriber, "audiences": audiences})


@login_required
def subscriber_delete(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, pk=subscriber_id, audience__user=request.user)
    if request.method == "POST":
        subscriber.delete()
        return redirect("subscribers")
    return render(request, "subscribers/subscriber_confirm_delete.html", {"subscriber": subscriber})


# ---------- EMAIL TEMPLATE VIEWS ----------

@login_required
def emailtemplate_list(request):
    templates = EmailTemplate.objects.filter(user=request.user)
    return render(request, "emailtemplates/emailtemplate_list.html", {"templates": templates})


@login_required
def emailtemplate_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        if name and subject and body:
            EmailTemplate.objects.create(user=request.user, name=name, subject=subject, body_text=body)
            return redirect("email_templates")
        else:
            return render(request, "emailtemplates/emailtemplate_form.html", {"error": "All fields are required."})
    return render(request, "emailtemplates/emailtemplate_form.html")


@login_required
def emailtemplate_update(request, template_id):
    template = get_object_or_404(EmailTemplate, pk=template_id, user=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        if name and subject and body:
            template.name = name
            template.subject = subject
            template.body_text = body
            template.save()
            messages.success(request, " Good Job! Template edited")
            return redirect("email_templates")
        else:
            return render(request, "emailtemplates/emailtemplate_form.html", {"template": template, "error": "All fields are required."})
    return render(request, "emailtemplates/emailtemplate_form.html", {"template": template})


@login_required
def emailtemplate_delete(request, template_id):
    template = get_object_or_404(EmailTemplate, pk=template_id, user=request.user)
    if request.method == "POST":
        template.delete()
        return redirect("email_templates")
    return render(request, "emailtemplates/emailtemplate_confirm_delete.html", {"template": template})


# ---------- CAMPAIGN VIEWS ----------

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.filter(user=request.user)
    return render(request, "campaigns/campaign_list.html", {"campaigns": campaigns})


@login_required
def campaign_create(request):
    audiences = Audience.objects.filter(user=request.user)
    templates = EmailTemplate.objects.filter(user=request.user)
    if request.method == "POST":
        subject = request.POST.get("name")
        audience_id = request.POST.get("audience")
        template_id = request.POST.get("template")

        scheduled_time = request.POST.get("scheduled_time")  # You might want to parse datetime
        if subject and audience_id and template_id:
            audience = get_object_or_404(Audience, pk=audience_id, user=request.user)
            template = get_object_or_404(EmailTemplate, pk=template_id, user=request.user)
            Campaign.objects.create(user=request.user, subject=subject, audience=audience, template=template, scheduled_time=scheduled_time)
            return redirect("campaigns")
        else:
            return render(request, "campaigns/campaign_form.html", {"audiences": audiences, "templates": templates, "error": "All fields are required."})
    return render(request, "campaigns/campaign_form.html", {"audiences": audiences, "templates": templates})

@login_required
def senddraft(request, campaign_id):
    campaigns = get_object_or_404(Campaign, pk = campaign_id, user = request.user)
    subscribers = Subscriber.objects.values_list('email', flat=True)
    if request.method =="POST":
        email = EmailMessage(subject="Wanjos testing",
                             body = 'sdgjkdbkjdb',
                             from_email = "hsdijkhs@gmail.com",
                             to = subscribers,
                             bcc=list(subscribers)
                             )
        email.send(fail_silently=False)

        if email.send():
            campaigns.status = "sent"
            campaigns.checks = "True"
            campaigns.save()
    return render(request, "campaigns/campaign_form.html")



@login_required
def campaign_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    audiences = Audience.objects.filter(user=request.user)
    templates = EmailTemplate.objects.filter(user=request.user)
    if request.method == "POST":
        subject = request.POST.get("subject")
        audience_id = request.POST.get("audience")
        template_id = request.POST.get("template")
        scheduled_time = request.POST.get("scheduled_time")
        if subject and audience_id and template_id:
            audience = get_object_or_404(Audience, pk=audience_id, user=request.user)
            template = get_object_or_404(EmailTemplate, pk=template_id, user=request.user)
            campaign.subject = subject
            campaign.audience = audience
            campaign.email_template = template
            campaign.scheduled_time = scheduled_time
            campaign.save()
            return redirect("campaign_list")
        else:
            return render(request, "campaigns/campaign_form.html", {"campaign": campaign, "audiences": audiences, "templates": templates, "error": "All fields are required."})
    return render(request, "campaigns/campaign_form.html", {"campaign": campaign, "audiences": audiences, "templates": templates})


@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if request.method == "POST":
        campaign.delete()
        return redirect("campaign_list")
    return render(request, "campaigns/campaign_confirm_delete.html", {"campaign": campaign})


# ---------- EMAIL LOG VIEWS ----------

@login_required
def emaillog_list(request):
    logs = EmailLog.objects.filter(user=request.user).order_by("-sent_at")
    return render(request, "emaillogs/emaillog_list.html", {"logs": logs})

# send mail to subscribers

def send(request):
    subs = Subscriber.objects.all()
    for mail in subs:
        emails = mail.email
    
    sending = EmailMessage(
        subject = "ojkl",
        body = "message",
       from_email = settings.EMAIL_HOST_USER,
       to = [emails],
       )
    sending.content_subtype = "html"
    sending.send(fail_silently=False,)
   
    return render(request, "subscribers/sendmail.html")
