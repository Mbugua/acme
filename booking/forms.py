from django import forms
# from django.contrib.auth.forms import AuthenticationForm
from .models import Ticket
import phonenumbers


class TicketForm(forms.ModelForm):
    '''
    Class to create a form for a user to get a ticket
    '''
    # phone_number = forms.CharField(max_length = 255)

    class Meta:
        model = Ticket

        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def clean(self):

        cleaned_data = super(TicketForm, self).clean()

        gotten_phone_number = cleaned_data.get('phone_number')

        # Check if phone number begins with the  country code
        if gotten_phone_number[:4] == '+254':

            # print('country code detected')

            # Convert string to phone number
            string_to_phonenumber = phonenumbers.parse(
                gotten_phone_number, "KE")

            print(len(gotten_phone_number))

            # Check if the phonenumber is not a valid  number
            if phonenumbers.is_possible_number(string_to_phonenumber) != True or len(gotten_phone_number) != 13:

                # print('Not a valid  number')
                raise forms.ValidationError(
                    'The phone number is not a valid  phone number')

        # Check if the number begins with a 0
        elif gotten_phone_number[:2] == '07':

            # print('number without country code')

            # Phone number string without 0
            without_zero = gotten_phone_number[1:]

            # Add  country code to the beginning
            add_country_code = '+254' + without_zero

            # Convert string to phone number
            string_to_phonenumber = phonenumbers.parse(add_country_code, "KE")

            # Check if the phonenumber is not a valid  number
            if phonenumbers.is_possible_number(string_to_phonenumber) != True or len(add_country_code) != 13:

                # print('Not a valid  number')
                raise forms.ValidationError(
                    'The phone number is not a valid  phone number')

        # Otherwise
        else:

            # print('number with non- country code')
            raise forms.ValidationError(
                'The phone number is not a valid  phone number')

        return cleaned_data
