from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, View

from account.forms import SignUpForm
from account.models import User, Contact, ActivationCode
from account.tasks import send_emial_aync
from django.urls import reverse_lazy
from django.conf import settings

from django.core.mail import send_mail


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email', 'first_name', 'last_name')
    success_url = reverse_lazy('index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)


class ContactUs(CreateView):
    template_name = 'contact.html'
    queryset = Contact.objects.all()
    fields = ('email', 'subject', 'text')
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        response = super().form_valid(form)
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('text')
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [form.cleaned_data.get('email'), ]
        send_emial_aync.delay(subject, message, email_from, recipient_list)
        return response


class SignUpView(CreateView):
    template_name = 'signup.html'
    queryset = User.objects.all()
    # fields = ('email', 'first_name', 'last_name', 'avatar',)
    success_url = reverse_lazy('index')
    form_class = SignUpForm


class Activate(View):
    def get(self, request, activation_code):
        ac = get_object_or_404(
            ActivationCode.objects.select_related('user'),
            code=activation_code, is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')
