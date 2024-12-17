from django import forms
from core.models import Comments
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm

class CommentForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': "Write review", 
            'class': 'form-control mb-3',
            'id': 'reviewer-text',
            'style': 'width: 100%; max-width: 300px;',
            'rows': 3,
        }))

    class Meta:
        model = Comments
        fields = ['review']

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label=_("Old Password"),
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': "Old password"})
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': "New password"})
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': "Confirm Password"})
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user  # Store user instance
        super().__init__(*args, **kwargs)  # Call the superclass's __init__

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("The old password you entered is incorrect."))
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(_("The new passwords do not match."))
        
        return cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data["new_password1"])
        self.user.save()  # Save the user instance
        return self.user

class DeactivateAccountForm(forms.Form):
    password = forms.CharField(label=_("Enter your password"), 
    widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': "Deactivate account"}))
