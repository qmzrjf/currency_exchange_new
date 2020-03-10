from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView
from account.models import User, Contact
from account.tasks import send_emial_aync
from django.urls import reverse_lazy
from django.conf import settings

from django.core.mail import send_mail


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email',)
    success_url = reverse_lazy('index')


class ContactUs(CreateView):
    template_name = 'contact.html'
    queryset = Contact.objects.all()
    fields = ('email', 'subject', 'text')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('text')
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [form.cleaned_data.get('email'), ]
        print(self.object)
        send_mail(subject, message, email_from, recipient_list)
        # send_emial_aync.delay(subject, message, email_from, recipient_list)

        return response
