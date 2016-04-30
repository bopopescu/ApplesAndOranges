import requests
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from djoser import utils
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


User = get_user_model()


class ResetPasswordForm(forms.Form):

    password1 = forms.CharField(label="New password",
                                widget=forms.PasswordInput(),
                                min_length=6,
                                max_length=25)
    password2 = forms.CharField(label="Retype password",
                                widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'password1',
            'password2',
            Submit('Change', 'submit'),
        )

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError(
                "You must type the same password each time.")
        return cleaned_data


class UserTokenForm(forms.Form):

    uid = forms.CharField()
    token = forms.CharField()

    user = None
    token_generator = default_token_generator

    error_messages = {
        'token_invalid': 'The password reset token was invalid.',
    }

    def _get_user(self, uid):
        try:
            pk = utils.decode_uid(uid)
            return User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            return None

    def clean(self):
        cleaned_data = super().clean()

        uid = cleaned_data['uid']
        token = cleaned_data['token']

        self.user = self._get_user(uid)
        if (self.user is None or
                not self.token_generator.check_token(self.user, token)):
            raise forms.ValidationError(self.error_messages['token_invalid'])

        return cleaned_data


class ResetPasswordView(FormView):
    template_name = 'auth/reset_password.html'
    success_url = reverse_lazy('password_reset_success')
    form_class = ResetPasswordForm

    def dispatch(self, request, uid, token, *args, **kwargs):
        token_form = UserTokenForm(data={'uid': uid, 'token': token})

        if not token_form.is_valid():
            return self.render_to_response(
                self.get_context_data(token_fail=True)
            )
        else:
            self.user = token_form.user
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.user.set_password(form.cleaned_data['password1'])
        self.user.save()
        return super().form_valid(form)


def activate_view(request, uid, token):
    # perform POST API request to activate user through API layer

    payload = {'uid': uid, 'token': token}

    pk = utils.decode_uid(uid)
    print(pk)
    try:
        target = User.objects.get(pk=pk)
        print(target)
        target.is_email_verified = True
        target.save()
        message = 'Your account has been activated, thanks for using Hillotask.'
    except:
        message = 'There is something wrong with activating your account. Please visit hillotask.com/support for additional help.'

    # if all is good
    # if resp.status_code == 200:
    #     message = 'Your account has been activated!'
    # else:
    #     message = 'There is something wrong with activating your account!'

    return render(request, 'auth/activate.html', {'message': message})
