from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, View, FormView

from account.forms import SignUpForm, ActivateForm
from account.models import User, Contact, ActivationCode, SmsCode
from account.tasks import send_emial_aync
from django.urls import reverse_lazy
from django.conf import settings

from django.core.mail import send_mail


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email', 'first_name', 'last_name', 'avatar')
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


    def get_success_url(self):
        self.requestsession['user_id'] = self.object.id
        return super().get_success_url()


class Activate(FormView):
    form_class = ActivateForm
    template_name = 'signup_sms.html'


    def post(self, request):
        user_id = request.session['user_id']
        sms_code = request.POST['sms_code']
        ac = get_object_or_404(
            SmsCode.objects.select_related('user'),
            code=sms_code,
            user_id=user_id,
            is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('activate')



