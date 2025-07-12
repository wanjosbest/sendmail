from django.contrib import admin
from .models import (Audience, Subscriber, EmailTemplate, Campaign, EmailLog, User,NewsletterSubscriber)




# Register customized User admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'audience', 'subscribed', 'subscribed_at', 'unsubscribed_at')
    search_fields = ('email', 'name')
    list_filter = ('subscribed', 'subscribed_at')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',  'subscribed', 'subscribed_at', 'unsubscribed_at')
    search_fields = ('email', 'name')
    list_filter = ('subscribed', 'subscribed_at')

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'subject', 'created_at')
    search_fields = ('name', 'subject', 'user__username')
    list_filter = ('created_at',)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'audience', 'status', 'scheduled_time', 'sent_time', 'created_at')
    search_fields = ('subject', 'user__username')
    list_filter = ('status', 'scheduled_time', 'sent_time', 'created_at')


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'subscriber', 'status', 'sent_at', 'opened_at', 'clicked_at')
    search_fields = ('subscriber__email', 'campaign__subject')
    list_filter = ('status', 'sent_at', 'opened_at', 'clicked_at')
