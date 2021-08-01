from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import pandas
from io import BytesIO


from .models import Poll, PollCategory, Candidate, PollCategoryGroup, RestrictionKey, Vote
from .forms import PollForm, CandidateForm, EditPollForm, KeyForm

# Page of active and unhidden polls
def index(request):
    polls = Poll.objects.filter(active=True, hidden=False)
    paginator = Paginator(polls, 10) # Show 10 items per page.
    page_number = request.GET.get('page')
    polls = paginator.get_page(page_number)
    context ={
        "polls":polls,
        "page":"home"
    }
    return render(request, "polls/index.html",context)

# Index of all created polls and add new poll form
@login_required(login_url = 'user:login')
def my_polls(request):
    form = PollForm()
    error_messages = []
    
    # Create a new poll
    if request.method == "POST":
        # # Limit number of user polls to 3
        # if Poll.objects.filter(creator = request.user).count() > 2:
        #     error_messages.append("User can only create a maximum of 3 polls")

        form = PollForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Poll.objects.create(
                    creator = request.user,
                    name = form.cleaned_data['name'],
                    image = form.cleaned_data['image'] ,
                    closing_date = form.cleaned_data['closing_date'],
                    restrictionType = form.cleaned_data['restrictionType'],
                    live_results = form.cleaned_data['live_results'] 
                )
                return HttpResponseRedirect(reverse('polls:my_index'))
            except Exception as e:
                error_messages.append(e)
                print(e)
        else:
            for field in form:   
                for error in field.errors:   
                    error_messages.append(error.capitalize())

    polls = Poll.objects.filter(creator = request.user)
    paginator = Paginator(polls, 10) # Show 10 items per page.
    page_number = request.GET.get('page')
    polls = paginator.get_page(page_number)

    context ={
        "form":form,
        "polls":polls,
        "error_messages":error_messages,
        "page":"myPolls"
    }
    return render(request, "polls/my_index.html",context)

# Get available groups for the poll, returned as json
@login_required(login_url = 'user:login')
def get_groups(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)
    groups = poll.groups.all()
    return JsonResponse([group.serialize() for group in groups],safe=False)

# Get available candidates for the selected category, returned as json
@login_required(login_url = 'user:login')
def get_candidates(request,poll_name,category_name):
    poll_name = poll_name.lower()
    category_name = category_name.lower()
    category = PollCategory.objects.get(poll__name = poll_name, name = category_name)
    candidates = category.candidates.all()
    return JsonResponse([candidate.serialize() for candidate in candidates],safe=False)

# Get available categories for the poll either all or by the group selected, returned as json
@login_required(login_url = 'user:login')
def get_categories(request,poll_name,group_name):
    poll_name = poll_name.lower()
    group_name = group_name.lower()
    poll = Poll.objects.get(name = poll_name)
    if group_name == "none":
        categories = poll.categories.all()
    else:   
        group= poll.groups.all().get(name = group_name)
        categories = group.categories.all()
    return JsonResponse([category.serialize() for category in categories],safe=False)

# Manage poll settings, groups, categories and candidates
@login_required(login_url = 'user:login')
def poll_management(request,poll_name,view):
    poll_name = poll_name.lower()
    view = view.lower()
    poll = Poll.objects.get(name = poll_name)
    poll.deadline() # check and update poll status considering the poll deadline
    # Check for creator and give access or deny
    if poll.creator != request.user:
        raise Http404
    # Default view is categories if none of the accepted views is provided
    if view != "categories" and view !="candidates" and view != "settings":
        view = "categories"
    context ={
        "view":view,
        "poll":poll,
    }
    return render(request, "polls/management.html",context)

# Handle api requests to poll categories for creation, editing, deleting of poll category
@login_required(login_url = 'user:login')
def manage_categories(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)

    # Check for creator and give access
    if poll.creator != request.user:
        raise Http404
    # Return poll categories in json
    if request.method == "GET":
        categories = poll.categories.all()
        return JsonResponse([category.serialize() for category in categories],safe=False)

    # Can only edit, create and delete only inactive polls
    if poll.active:
        return HttpResponse(status = 403)
    elif request.method == "POST":
        data = json.loads(request.body)
        # Get new polls name from json data
        name = data['name']
        # Default group selected to none
        group = None
        # Get the group object if a group was provided
        if data['group']:
            try:
                group = poll.groups.all.get(name = data["group"])
            except Exception as e:
                print(e)
        # Check against empty name and then save new poll
        if name.split():
            try:
                PollCategory.objects.create(
                    poll = poll,
                    name = name,
                    group = group
                )
                return HttpResponse(status = 201)
            except Exception as e:
                print(e)
                return HttpResponse(status = 400)

    # Editing an already existing category
    elif request.method == "PUT":
        data = json.loads(request.body)
        # Select category by id provided
        category_id = data['id']
        category = poll.categories.all().get(id = category_id)
        
        # Request to remove link of all candidates to this category
        if data['action'] == "clear_candidates":
            candidates = category.candidates.all()
            for candidate in candidates:
                candidate.categories_contesting.remove(category)
            return HttpResponse(status = 201)
        
        # Handle replacing category name and also changing the group it is under
        new_name = data['name']
        new_group_name = data['group_name']

        if new_name.split():
            category.name = new_name
        if new_group_name:
            new_group = poll.groups.all().get(name = new_group_name)
            category.group = new_group
        try:
            category.save()
            return HttpResponse(status = 201)
        except Exception as e:
            print(e)
            return HttpResponse(status=400)

    # Delete category from the poll
    elif request.method == "DELETE":
        data = json.loads(request.body)
        category_id = data['id']
        category = poll.categories.all().get(id = category_id)
        category.delete()
        return HttpResponse(status = 201)

# Handle access, creation and deletion of candidates to poll
@login_required(login_url = 'user:login')
def manage_candidates(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)

    # Check for creator and give access or deny
    if poll.creator != request.user:
        raise Http404
    
    # Return all candidates data in json 
    if request.method == "GET":
        candidates = poll.candidates.all()
        return JsonResponse([candidate.serialize() for candidate in candidates],safe=False)
    
    # Cannot edit or save candidate in an active poll
    if poll.active:
        return HttpResponse(status = 403)
        
    elif request.method == "POST":
        candidate_form = CandidateForm(request.POST , request.FILES)
        categories = request.POST["categories"].split(',')   
        print(request.POST['party'])
        if candidate_form.is_valid():
            print(candidate_form.cleaned_data["party"])
            # Create a new candidate
            if request.POST['form_type'] == "new_candidate":
                try:
                    candidate = Candidate.objects.create(
                        poll = poll,
                        name = candidate_form.cleaned_data["name"],
                        party = candidate_form.cleaned_data["party"],
                        image = candidate_form.cleaned_data["image"]
                    )
                    for category in categories:
                        try:
                            category = poll.categories.all().get(name = category)
                            candidate.categories_contesting.add(category)
                        except Exception as e:
                            print(e)
                    candidate.save()
                    return HttpResponse(status=201)
                except Exception as e:
                    print("error: ",e)

            # Edit an already existing candidate's data
            elif request.POST['form_type'] == "edit_candidate":
                candidate = poll.candidates.all().get(id = request.POST['candidate_id'])
                candidate.name = candidate_form.cleaned_data["name"]
                candidate.party = candidate_form.cleaned_data["party"] 
                new_image = candidate_form.cleaned_data["image"]
                candidate.categories_contesting.clear()
                if new_image:
                    candidate.image = new_image
                for category in categories:
                    try:
                        category = poll.categories.all().get(name = category)
                        candidate.categories_contesting.add(category)
                    except Exception as e:
                        print(e)
                candidate.save()
                
                return HttpResponse(status=201)
        else:
            print(candidate_form.errors)
    # Delete candidate   
    elif request.method == "DELETE":
        data = json.loads(request.body)
        candidate_id = data['id']
        candidate = poll.candidates.all().get(id = candidate_id)
        candidate.delete()
        return HttpResponse(status=201)
    return HttpResponse(status = 400)

# Handles editing poll data, groups, status(active,hidden), deadline and restriction type
@login_required(login_url = 'user:login')
def manage_settings(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)

    # Check for creator and give access or deny
    if poll.creator != request.user:
        raise Http404
    # Return data of data in json
    if request.method == "GET":
        return JsonResponse(poll.serialize(),safe=False)

    if request.method == "POST":
        # Cannot alter the data, restriction type and deadline of an active poll
        if poll.active:
            return HttpResponse(status = 403)

        # Change name, picture, or restriction type
        if request.POST['action'] == "edit_poll":
            form = EditPollForm(request.POST , request.FILES)
            if form.is_valid():
                try:
                    poll.name = form.cleaned_data['name']
                    if form.cleaned_data["image"]:
                        poll.image = form.cleaned_data["image"]
                    poll.restrictionType =  form.cleaned_data["restrictionType"]
                    poll.closing_date = form.cleaned_data["closing_date"]
                    poll.live_results = form.cleaned_data["live_results"]
                    poll.save()
                    return HttpResponse(status = 201)
                except Exception as e:
                    print(e)
            else:
                print(form.errors)

        # Create a new group
        elif request.POST['action'] == "new_group":
            name = request.POST['name']
            if name.split():
                try:
                    PollCategoryGroup.objects.create(
                        poll = poll,
                        name = name
                    )
                    return HttpResponse(status = 201)
                except Exception as e:
                    print("Exception:",e)
            return HttpResponse(status = 400)

    # Change status(active,hidden) or edit existing group of poll
    elif request.method == "PUT":
        data = json.loads(request.body)
        action = data['action']
        activity = data['activity']
        print(data)
        if action == "hide":
            poll.hidden = activity
            poll.save()

        elif action == "launch":
            if activity:
                try:
                    poll.launch()
                except Exception as e:
                    return JsonResponse({"error":str(e)},safe=False,status=400)
            else:
                poll.active = activity
                poll.save()

        elif action == "edit_group":
            if poll.active:
                return HttpResponse(status = 403)
            group = poll.groups.all().get(id = data["group_id"])
            if data["group_new_name"].split():
                group.name = data["group_new_name"]
                group.save()
            else:
                return HttpResponse(status = 400)
        return HttpResponse(status = 201)
    
    # Delete inactive poll or delete a group
    elif request.method == "DELETE":
        if poll.active:
            return HttpResponse(status = 403)
        data = json.loads(request.body)
        action = data['action']
        if action == "group":
            group_name = data['name']
            group = poll.groups.all().get(name = group_name)
            group.delete()
            return HttpResponse(status = 201)
        elif action == "poll":
            poll.delete()
            return HttpResponse(status = 201)
    return HttpResponse(status = 400)

# Create or delete keys to access poll
@login_required(login_url = 'user:login')
def poll_keys(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)

    # Check for creator and give access or deny
    if poll.creator != request.user:
        raise Http404

    # Return json of all keys
    if request.method == "GET":
        return JsonResponse([key.serialize() for key in poll.keys.all()],safe=False)

    # Cannot edit keys of an active poll
    if poll.active:
        return HttpResponse(status = 403)

    # Create a new key
    if request.method == "POST":
        data = json.loads(request.body)
        form = KeyForm(data)
        if form.is_valid():
            try:
                RestrictionKey.objects.create(
                    poll = poll,
                    key = form.cleaned_data["key"],
                )
                return HttpResponse(status = 201)

            except Exception as e:
                print("Exception on Key: ", e)   
        else:
            print(form.errors)

    # Delete a key
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            key = RestrictionKey.objects.get(id = data["key_id"])
            key.delete()
            return HttpResponse(status = 201)
        except Exception as e:
            print(e)
    return HttpResponse(status = 400)
        
# Add keys from excel spreadsheet or print keys to excel
@login_required(login_url = 'user:login')    
def excel_keys(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)

    # Check for creator and give access or deny
    if poll.creator != request.user:
        raise Http404
    # Return keys as excel spreadsheet download
    if request.method == "GET":
        keys = poll.keys.all()
        df = pandas.DataFrame([key.key for key in keys])
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pandas.ExcelWriter(b, engine='openpyxl')
            df.to_excel(writer, sheet_name=f'{poll.name.upper()}-KEYS', index=False)
            writer.save()
            # Set up the Http response.
            filename = f'{poll.name.upper()}-KEYS.xlsx'
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
    # Add keys from spreadsheet
    if request.method == "POST":
        print("excel upload")
        sheet = request.FILES.get('sheet',False)
        raw_data = pandas.read_excel(sheet, header=None)
        for i, row in raw_data.iterrows():
            if row.notnull().all():
                data = raw_data.iloc[(i+1):].reset_index(drop=True)
                data.columns = list(raw_data.iloc[i])
                break
        # transforming columns to numeric where possible
        for c in data.columns:
            data[c] = pandas.to_numeric(data[c], errors='ignore')
        header_choice = data.columns.values[0]
        if header_choice:
            for i in data[header_choice]:
                key = i
                # Create Key
                if key.split():
                    try:
                        RestrictionKey.objects.create(
                            poll = poll,
                            key = key,
                        )
                    except Exception as e:
                        print("Exception on Key: ", e)
        return HttpResponse(status = 201)
    raise Http404

# Accessing actual voting page of poll
@login_required(login_url = 'user:login')
def votingPage(request,poll_name,preview=False):
    print(preview)
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)
    poll.deadline()
    # If poll is inactive and user is not creator then deny access
    if not poll.active and not poll.creator == request.user:
        raise Http404
        
    if poll.active:
        preview = False
    
    if not preview:
        # Check if access key required
        if poll.active:
            if poll.restrictionType == "oneKey":
                try:
                    RestrictionKey.objects.get(poll=poll , allowed = request.user)
                except RestrictionKey.DoesNotExist:
                    return HttpResponseRedirect(reverse("polls:input_key",kwargs={"poll_name":poll_name}))
            elif poll.restrictionType == "specialKeys":
                try:
                    RestrictionKey.objects.get(poll=poll , usedBy = request.user)
                except RestrictionKey.DoesNotExist:
                    return HttpResponseRedirect(reverse("polls:input_key",kwargs={"poll_name":poll_name}))
    context ={
        "poll_name":poll_name,
        "poll":poll,
        "preview":preview
    }
    return render(request, "polls/voting.html",context)

# Input access key page
@login_required(login_url = 'user:login')
def input_key(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)
    error_message = ""
    
    # If an already verified user tries to access page redirect to voting page 
    try:
        RestrictionKey.objects.get(poll=poll , usedBy = request.user)
        return HttpResponseRedirect(reverse("polls:voting_page",kwargs={"poll_name":poll_name}))
    except RestrictionKey.DoesNotExist:
        pass

    if request.method == "POST":
        key = request.POST["key"]
        print(key)
        
        # Add user to verified users(allowed)
        if poll.restrictionType == "oneKey" :
            print(poll.restrictionType)
            try:
                restriction_key = RestrictionKey.objects.get(poll = poll, key = key)
                restriction_key.allowed.add(request.user)
                restriction_key.save()
                print("reusable key used")
                return HttpResponseRedirect(reverse("polls:voting_page",kwargs={"poll_name":poll_name}))
            except Exception as e:
                error_message = "Incorrect Key"

        # Verify user key and remove key from being used again
        elif poll.restrictionType == "specialKeys":
            print(poll.restrictionType)
            try:
                # restriction_key = RestrictionKey.objects.filter(poll = poll, usedBy= not None )
                restriction_key = RestrictionKey.objects.get(poll = poll, key = key, usedBy= None )
                print(restriction_key.key)
                restriction_key.usedBy = request.user
                restriction_key.save()
                print("special key used")
                return HttpResponseRedirect(reverse("polls:voting_page",kwargs={"poll_name":poll_name}))
            except Exception as e:
                print(e)
                error_message = "Incorrect Key"

    context ={
        "poll_name":poll_name,
        "error_message": error_message
    }
    return render(request, "polls/input_key.html",context)

# User attempt to vote
@login_required(login_url = 'user:login')
def vote(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)

    # Check poll deadline and update
    poll.deadline()
    
    # Can't vote in inactive poll
    if not poll.active:
        return HttpResponse(status = 403)
    
    # Register user's vote
    if request.method == "POST":
        data = json.loads(request.body)
        category_name = data.get("category_name").lower() 
        candidate_id = data.get("candidate_id") 
        try:
            Vote.objects.create(
                voter = request.user,
                poll = poll,
                category = PollCategory.objects.get(poll = poll, name = category_name),
                candidate = Candidate.objects.get(poll = poll, id = candidate_id)
            )
            return HttpResponse(status = 201)
        except Exception as e:
            print(e)
            return HttpResponse(status = 403)

# Index of all polls user participated in, redirect to results
@login_required(login_url = 'user:login')
def results_index(request):
    results_interested = request.user.voted_polls.all().values('poll__name').distinct()
    
    # polls = Poll.objects.filter(name__in = results_interested, active=False)
    polls = Poll.objects.filter(name__in = results_interested)
    print(polls)

    context = {
       "polls" : polls,
        "page":"results"

    }
    return render(request, 'polls/results_index.html', context)

# Results Page of poll
@login_required(login_url = 'user:login')
def resultsPage(request,poll_name):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)
    if poll.active and not poll.live_results:
        raise Http404
   
    context = {
        "poll_name":poll.name,
        "image":poll.image,
        "poll_active":poll.active,
    }
    return render(request, 'polls/results.html', context)

# Results of poll
@login_required(login_url = 'user:login')
def results(request,poll_name,category_name,sort):
    poll_name = poll_name.lower()
    poll = Poll.objects.get(name = poll_name)
    if poll.active and not poll.live_results:
        raise Http404
    category = PollCategory.objects.get(poll=poll, name =category_name )
    if sort == "yes":
        return JsonResponse(category.resultsByVotes(),safe=False)
    return JsonResponse(category.results(),safe=False)

