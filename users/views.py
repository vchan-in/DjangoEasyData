from multiprocessing import context
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import UsersDetails
from .models import Ser

from .forms import UserDetailForm

import requests, json
from django.conf import settings

import uuid
import time
import os
import base64
from hashlib import sha256
from uuid import UUID

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def generate_nonce():
    # Return
    # return os.urandom(16)
    # return base64.b64encode(os.urandom(16)).decode('utf-8')
    nonce = os.urandom(16)
    return base64.b64encode(nonce).decode('utf-8')

def generate_created():
    return time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())

def generate_password(nonce, timestamp, client_password):
    nonce_bytes = base64.b64decode(nonce)
    timestamp_bytes = timestamp.encode()
    client_password_bytes = client_password.encode()
    hash_object = sha256(nonce_bytes + timestamp_bytes + client_password_bytes)
    return base64.b64encode(hash_object.digest()).decode()

#List
def create_view(request):
    # User Detail fields
    if request.method == "POST":
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        credit_card = request.POST.get("credit_card")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        

        uuid_cc = uuid.uuid4().hex # Generate new UUID for credit card
        uuid_email = uuid.uuid4().hex # Generate new UUID for email
        client_username = settings.RANDTRONICS_EASYDATA_CLIENT_USERNAME
        created = generate_created()
        nonce = generate_nonce()
        client_password = generate_password(nonce, created, settings.RANDTRONICS_EASYDATA_CLIENT_PASSWORD)


        # Generate new AES 256 key using Randtronics DPM easyData API
        url = settings.RANDTRONICS_EASYDATA_API + "/DpmTokenManagerCoreEngine/tokenmanagerRestful/doTokenization"

        payload_cc = {
            "policyName": "DemoAppNewCC",
            "dataList": {
                "dataItem": [
                    {
                        "identifier": uuid_cc,
                        "inputData": credit_card
                    }
                ]
            }
        }

        payload_email = {
            "policyName": "DemoAppNewEmail",
            "dataList": {
                "dataItem": [
                    {
                        "identifier": uuid_email,
                        "inputData": email
                    }
                ]
            }
        }

        headers = {
            "Content-Type": "application/json",
            "username": client_username,
            "created": created,
            "nonce": nonce,
            "password": client_password


        }

        print("Request headers: ", headers)
        
        response_cc = requests.request("POST", url, headers=headers, json=payload_cc, verify=False)
        response_email = requests.request("POST", url, headers=headers, json=payload_email, verify=False)
        
        print("Response CC: ", response_cc.text)
        
        try:
            response_cc_json = response_cc.json()
            response_email_json = response_email.json()
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            print("Response CC: ", response_cc.text)
            print("Response Email: ", response_email.text)
            # Handle the error appropriately here
            response_cc_json = {}
            response_email_json = {}

        if response_cc_json and response_email_json:
            tokenized_cc = response_cc_json["responseDetails"][0]["token"]
            tokenized_email = response_email_json["responseDetails"][0]["token"]

            # Create User Detail
            user = UsersDetails(
                name=name,
                gender=gender,
                phone=phone,
                credit_card=tokenized_cc,
                username=username,
                email=tokenized_email,
                password=password,
                uuid_cc=uuid_cc,
                uuid_email=uuid_email,
            )
            user.save()
            return HttpResponseRedirect("/") # Redirect to list_view
    else:
        genders = ["Male", "Female", "Other"]
        context = {
            "genders": genders
        }
        return render(request, "create_view.html", context)

#List
def list_view(request):

    get_data = UsersDetails.objects.all()

    ids = []
    names = []
    genders = []
    phones = []  
    credit_cards = []
    usernames = []
    emails = []
    passwords = []
    for data in get_data:
        ids.append(data.id) 
        names.append(data.name)
        genders.append(data.gender)
        phones.append(data.phone)

        client_username = settings.RANDTRONICS_EASYDATA_CLIENT_USERNAME
        created = generate_created()
        nonce = generate_nonce()
        client_password = generate_password(nonce, created, settings.RANDTRONICS_EASYDATA_CLIENT_PASSWORD)


        if data.uuid_cc != "" and data.uuid_email != "":
            # Decrypt credit card number and email and password using AES 256 key
            url = settings.RANDTRONICS_EASYDATA_API + "/DpmTokenManagerCoreEngine/tokenmanagerRestful/doDetokenization"
            
            payload_cc = { 
                "policyName": "DemoAppNewCC",
                "dataList": {
                    "dataItem": [
                        {
                            "identifier": data.uuid_cc,
                            "token": data.credit_card
                        }
                    ]
                }
            }

            payload_email = {
                "policyName": "DemoAppNewEmail",
                "dataList": {
                    "dataItem": [
                            {
                                "identifier": data.uuid_email,
                                "token": data.email
                            }
                    ]
                }
            }

            headers = {
                "Content-Type": "application/json",
                "username": client_username,
                "created": created,
                "nonce": nonce,
                "password": client_password
            }

            response_cc = requests.request("POST", url, headers=headers, json=payload_cc, verify=False)
            response_email = requests.request("POST", url, headers=headers, json=payload_email, verify=False)

            detokenized_cc = response_cc.json()["responseDetails"][0]["originalValue"]
            detokenized_email = response_email.json()["responseDetails"][0]["originalValue"]

            credit_cards.append(detokenized_cc)
            emails.append(detokenized_email)
        else:
            credit_cards.append(data.credit_card)
            emails.append(data.email)
        usernames.append(data.username)
        passwords.append(data.password)

    all_data = []
    for i in range(len(ids)):
        all_data.append({"id": ids[i],
                            "name": names[i],
                            "gender": genders[i],
                            "email": emails[i],
                            "phone": phones[i],
                            "credit_card": credit_cards[i],
                            "username": usernames[i],
                            "password": passwords[i]})
    context = {
        "all_data": all_data
    }
    return render(request, "list_view.html", context)
    

#Update
def detail_view(request, id):

    context = {}

    context["data"] = UsersDetails.objects.get(id = id)

    return render(request, "detail_view.html", context)

#update
def update_view(request, id):

    context = {}

    obj = get_object_or_404(UsersDetails, id=id)

    form = UserDetailForm(request.POST or None, instance = obj)

    if form.is_valid():

        form.save()

        return HttpResponseRedirect("/"+id)

    context["form"] = form

    return render(request, "update_view.html", context)

#Delte
def delete_view(request, id):

    context = {}

    obj = get_object_or_404(UsersDetails, id = id)

    if request.method == "POST":

        obj.delete()

        return HttpResponseRedirect("/")

    return render(request, "delete_view.html", context)



