from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from djoser import settings as djoser_settings
from djoser.utils import SendEmailViewMixin

from _commons.admin.mixins import (NonEditableInline, FkAdminLink,
                                   ReadOnlyFieldsFromFieldsets)
from _commons.notifications import EmailNotification, PushNotification

from tasks.models import Task, Tasker
from .models import AppUser, University, Language


class CustomUserCreationForm(SendEmailViewMixin, forms.ModelForm):
    """Form for creating user using admin interface.

    This form:
        make field `email` required and validates that email belongs to
            universities
        add fields `first_name`, `last_name`, `birthday`, `avatar` as required
        sets user's university based on email
        sets username be the same as email
        send activation email
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    avatar = forms.ImageField(required=True)

    # settings for Activation email (handled by SendEmailViewMixin from
    # djoser app)
    token_generator = default_token_generator
    subject_template_name = 'activation_email_subject.txt'
    plain_body_template_name = 'activation_email_body.txt'

    class Meta:
        model = AppUser
        fields = ('email', 'birthday', 'password', 'first_name', 'last_name',
                  'avatar')
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_email(self):
        """Validate that email domain belongs to supported universities
        """
        email = self.cleaned_data.get("email")
        email = email.lower()
        domain = email.split('@')[1]
        try:
            self.university = University.objects.get(domain=domain.lower())
        except University.DoesNotExist:
            raise ValidationError(
                'You haven\'t provide email address that belongs to one of'
                'our supported universities: {}'.format(
                    ['@'+u.domain for u in University.objects.all()]))
        return email

    def get_email_context(self, user):
        """Get context for activation email (from Djoser app)
        """
        context = super().get_email_context(user)
        context['url'] = djoser_settings.get('ACTIVATION_URL').format(
            **context)
        return context

    def save(self, commit=True):
        """Save new user and set user's university based on provided email.
        Also send activation email
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.university = self.university
        user.username = user.email
        user.save()
        # send activation email (logic from Djoser app)
        self.send_email(**self.get_send_email_kwargs(user))
        return user


class TaskPosterInline(NonEditableInline, FkAdminLink, admin.TabularInline):
    model = Task
    fk_name = 'poster'
    readonly_fields = ('_url', '_poster', 'status', 'payment_option', 'budget', 'fee', 'earning',
                       '_tasker', 'created', 'updated', 'completed')
    fields = readonly_fields
    verbose_name_plural = "Posted Tasks"

    def _url(self, obj):
        return self._admin_url(obj, obj.id)
    _url.short_description = "Admin link"

    def _tasker(self, obj):
        return self._admin_url(obj.tasker)
    _tasker.short_description = "Tasker"

    def _poster(self, obj):
        return self._admin_url(obj.poster)
    _poster.short_description = "Poster"


class TaskTaskerInline(TaskPosterInline):
    fk_name = 'tasker'
    verbose_name_plural = "Assigned Tasks"


class TaskApplicantInline(NonEditableInline, FkAdminLink, admin.TabularInline):
    model = Tasker
    fk_name = 'user'
    verbose_name_plural = "Applied Tasks"
    readonly_fields = ('_url', '_poster', '_status', '_category', '_budget',
        '_tasker', 'created', 'updated')
    fields = readonly_fields

    def _url(self, obj):
        return self._admin_url(obj.task, obj.task.id)
    _url.short_description = "Admin link"

    def _poster(self, obj):
        return self._admin_url(obj.task.poster)
    _poster.short_description = "Poster"

    def _status(self, obj):
        return obj.task.get_status_display()
    _status.short_description = 'Status'

    def _category(self, obj):
        return obj.task.category.__str__()
    _category.short_description = 'Category'

    def _paymentOption(self, obj):
        return obj.task.payment_option.__str__()
    _paymentOption.short_description =  'Payment Option'

    def _budget(self, obj):
        return obj.task.budget
    _budget.short_description = 'Budget'

    def _earning(self, obj):
        return obj.task.earning
    _budget.short_description = 'Earning'

    def _tasker(self, obj):
        return self._admin_url(obj.task.tasker)
    _tasker.short_description = "Tasker"

    def _created(self, obj):
        return self._admin_url(obj.task.created)
    _created.short_description = "Created"

    def _updated(self, obj):
        return self._admin_url(obj.task.updated)
    _updated.short_description = "Updated"

class OfficialPushNotification(PushNotification):
    notification_name = 'Hillotask Official'

    def __init__(self, user=None):
        payload = {
            "message": "Cras et nisl fermentum, convallis nulla sit amet, \
                        tempus justo. Nulla facilisi. Nunc convallis mattis \
                        gravida. Cras at ipsum odio. Mauris vel urna augue. ",
            "sound": "default",
            "badge": 1,
            "extra":
                {
                    "type": "Hillotask.Official",
                    "title": "Hillotask Official Message Title",
                    "text": "Hillotask Official Message",
                    "user": user.id,
                    "username": user.username,
                    "full_name": user.full_name
                }
        }
        super().__init__(payload=payload)
        self.recepients = [user.id]
        # Run it
        self()


def make_refresh(ModelAdmin, request, queryset):
    for i in queryset:
        i.save()
make_refresh.short_description = "Refresh Selected User profile"

def make_official_announcement(ModelAdmin, request, queryset):
    for i in queryset:
        OfficialPushNotification(i)
make_official_announcement.short_description = "Sent Notification to Selected User"

class AppUserAdmin(FkAdminLink, UserAdmin):
    add_form = CustomUserCreationForm
    add_form_template = 'admin/change_form.html'
    list_display = ('email', 'id', 'full_name', 'personal_email', 'phone',
                    'major', 'is_active', 'is_email_verified', 'invite_code_counter')
    list_filter = ('university', 'is_active', 'is_email_verified', 'major', 'skills', 'standing')
    readonly_fields = ('age', 'last_login', 'date_joined',
                       '_likes', '_dislikes', '_tasker_rating', '_customer',
                       '_avatar_preview')
    search_fields = ('username', 'email', 'about', 'skills')
    actions = [make_refresh, make_official_announcement]
    ordering = ('email', )
    fieldsets = (
        ('Authorization', {
            'fields': ('email', 'password', 'is_email_verified',
                       '_customer')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'gender', 'phone',
                       'birthday', 'age', 'university', 'languages',
                       'major', 'standing', 'skills', 'about',
                       '_avatar_preview', 'avatar')
        }),
        ('Address info', {
            'fields': ('address1', 'address2', 'city', 'state', 'zip_code')
        }),
        ('Ratings', {
            'fields': ('_likes', '_dislikes', '_tasker_rating', )
        }),
        ('Activity', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Event', {
            'fields': ('invite_code', 'invite_code_counter')
        }),
    )
    add_fieldsets = (
        ('Authorization', {
            'fields': ('email', 'password'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'birthday', 'avatar', )
        }),
    )
    inlines = [TaskPosterInline, TaskTaskerInline, TaskApplicantInline]

    def _likes(self, obj):
        return obj.poster_rating_field.likes
    _likes.short_description = "Likes"

    def _customer(self, obj):
        return self._admin_url(obj.customer)
    _customer.short_description = "Customer"

    def _dislikes(self, obj):
        return obj.poster_rating_field.dislikes
    _dislikes.short_description = "Disikes"

    def _tasker_rating(self, user):
        return user.tasker_rating
    _tasker_rating.short_description = 'Tasker rating'

    def _avatar_preview(self, user):
        if user.avatar:
            return mark_safe(
                "<img src=\"{}\" style=\"max-height: 200px\">"\
                .format(user.avatar.url))
        else:
            return None
    _avatar_preview.short_description = "Avatar preview"

    def save_model(self, request, obj, form, change):
        """Update avatar thumbnail if new avatar was added
        """
        super().save_model(request, obj, form, change)
        new_avatar = request.FILES.get('avatar')
        if new_avatar:
            obj.avatar_thumbnail.delete()
            obj.avatar_thumbnail.save('avatarthumbnail', new_avatar)

    def get_form(self, request, obj=None, **kwargs):
        """Add current request to form
        """
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form


class UniversitiesAdmin(admin.ModelAdmin):
    list_filter = ('name', 'domain', )
    list_display = ('name', 'domain', 'location')
    ordering = ('name', )


class LanguagesAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    list_display = ('name', )
    ordering = ('name', )


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(University, UniversitiesAdmin)
admin.site.register(Language, LanguagesAdmin)
