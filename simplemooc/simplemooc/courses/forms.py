from django import forms
from django.core.mail import send_mail
from django.conf import settings
from simplemooc.core.mail import send_mail_template

from .models import Comment


class ContactCourse(forms.Form):

    name = forms.CharField(label="Nome", max_length=100)
    email = forms.EmailField(label="E-mail")
    msg = forms.CharField(
        label="Mensagem/Dúvida",
        widget=forms.Textarea
        )

# Modo Manual
    # def send_mail(self, course):
    #     subject = '[%s] Contato' % course
    #     message = 'Nome: %(name)s;E-mail: %(email)s;%(msg)s'
    #     context = {
    #         "name": self.cleaned_data["name"],
    #         "email": self.cleaned_data["email"],
    #         "msg": self.cleaned_data["msg"]
    #     }

    #     message = message % context
    #     send_mail(subject, message,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [settings.CONTACT_EMAIL])

    def send_mail(self, course):
        template_name = "courses/contact_email.html"
        subject = '[%s] Contato' % course

        context = {
            "name": self.cleaned_data["name"],
            "email": self.cleaned_data["email"],
            "msg": self.cleaned_data["msg"]
        }

        send_mail_template(subject, template_name,
                           context,
                           [settings.CONTACT_EMAIL])


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
