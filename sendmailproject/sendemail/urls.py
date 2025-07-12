from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    # Audience
    path('audiences/', views.audience_list, name='audiences'),
    path('audiences/create/', views.audience_create, name='audience_create'),
    path('audiences/import-contacts/', views.import_contact, name='import_contact'),
    path('audiences/<int:audience_id>/edit/', views.audience_update, name='audience_edit'),
    path('audiences/<int:audience_id>/delete/', views.audience_delete, name='audience_delete'),
    

    # Subscriber
    path('subscribers/', views.subscriber_list, name='subscribers'),
    path("newsletter/subscribe/", views.sub_newsletter, name="newsletter"),
    path('subscribers/create/', views.subscriber_create, name='subscriber_create'),
    path('subscribers/<int:subscriber_id>/edit/', views.subscriber_update, name='subscriber_edit'),
    path('subscribers/<int:subscriber_id>/delete/', views.subscriber_delete, name='subscriber_delete'),

    # Email Templates
    path('templates/', views.emailtemplate_list, name='email_templates'),
    path('templates/create/', views.emailtemplate_create, name='email_template_create'),
    path('templates/<int:template_id>/edit/', views.emailtemplate_update, name='email_template_edit'),
    path('templates/<int:template_id>/delete/', views.emailtemplate_delete, name='email_template_delete'),

    # Campaigns
    path('campaigns/', views.campaign_list, name='campaigns'),
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path('campaigns/<int:campaign_id>/edit/', views.campaign_update, name='campaign_edit'),
    path('campaigns/<int:campaign_id>/delete/', views.campaign_delete, name='campaign_delete'),
    path('senddraft/<int:campaign_id>/', views.senddraft, name="senddraft"),

    # Email Logs
    path('logs/', views.emaillog_list, name='email_logs'),
    path('send/', views.send, name='send'),
]
