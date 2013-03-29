# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User

from forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            
            # Should look into using a custom User model
            # in case email is longer than 30 chars
            #email_name = form.cleaned_data['email']

            password = form.cleaned_data['password']

            # Create the new user
            user = User.objects.create_user(email_name, email_name, password)

            # Log the new user in
            user = auth.authenticate(username=email_name, password=password)
            auth.login(request, user)
            
            # recipients = [email_name]
            # send_mail("Qcumber Signup", "Yay! You signed up.", sender, recipients)


            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = SignupForm() # An unbound form

    return render(request, 'registration/signup.html', {
        'form': form,
    })

