from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmação de Senha", 
                        widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "As senhas informadas não conferem",
                code="password_mismatch"
            )

            return password2
    
    def save(self, commit=True):    
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "name"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError("Já existe um usuário com este email")
        
        return email
