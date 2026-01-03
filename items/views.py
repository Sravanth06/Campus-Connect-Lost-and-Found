from django.core.mail import send_mail
from django.conf import settings
# Ensure 'from thefuzz import fuzz' is also there
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import SignUpForm, ItemForm
from thefuzz import fuzz  # AI Matching Library

def item_list(request):
    """Displays all lost and found items."""
    items = Item.objects.all().order_by('-date_reported')
    return render(request, 'items/item_list.html', {'items': items})

@login_required
@login_required
@login_required
@login_required
def report_item(request):
    """Handles reporting an item and sends CUSTOMIZED ALERTS to both parties."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Save the new item
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            
            # 2. AI LOGIC: Check for matches
            target_type = 'Found' if new_item.item_type == 'Lost' else 'Lost'
            candidates = Item.objects.filter(item_type=target_type)
            
            print(f"--> AI Engine Started. Checking {len(candidates)} candidates...")

            for candidate in candidates:
                # Calculate Score
                name_score = fuzz.partial_ratio(new_item.name.lower(), candidate.name.lower())
                desc_score = fuzz.token_set_ratio(new_item.description.lower(), candidate.description.lower())
                avg_score = (name_score + desc_score) / 2
                
                # 3. IF MATCH FOUND (>70%), SEND TWO EMAILS
                if avg_score > 70:
                    print("--------------------------------------------------")
                    print(f"✅ MATCH FOUND (Score: {avg_score}%)! Sending Dual Notifications...")

                    # --- Define the Custom Messages ---
                    msg_for_finder = "Thank you for being a responsible student! Please verify the claimer's identity carefully before handing over the item."
                    msg_for_owner = "Good news! This matches your lost item description. Please contact the finder immediately to verify and reclaim your belongings."

                    # --- EMAIL 1: To the Current User ---
                    # Determine if current user is the Finder or Owner
                    if new_item.item_type == 'Found':
                        current_footer = msg_for_finder
                    else:
                        current_footer = msg_for_owner

                    subject_current = f"Campus Connect: Match Found for '{new_item.name}'"
                    message_current = f"""
                    Hello {request.user.username},
                    
                    We found a match for the item you just reported: "{new_item.name}".
                    
                    DETAILS OF MATCH:
                    Item: {candidate.name}
                    Description: {candidate.description}
                    Contact Info: {candidate.contact_info}
                    
                    {current_footer}
                    """
                    send_mail(
                        subject_current,
                        message_current,
                        settings.EMAIL_HOST_USER,
                        [request.user.email], 
                        fail_silently=False,
                    )
                    print(f"   -> Notification sent to Current User ({new_item.item_type})")

                    # --- EMAIL 2: To the Previous User (Candidate Owner) ---
                    if candidate.user and candidate.user.email:
                        # Determine if previous user is the Finder or Owner
                        if candidate.item_type == 'Found':
                            candidate_footer = msg_for_finder
                        else:
                            candidate_footer = msg_for_owner

                        subject_other = f"Campus Connect: New Match for your '{candidate.name}'"
                        message_other = f"""
                        Hello {candidate.user.username},
                        
                        Great news! You previously reported a {candidate.item_type} item: "{candidate.name}".
                        Someone just posted a matching item!
                        
                        DETAILS OF NEW MATCH:
                        Item: {new_item.name}
                        Description: {new_item.description}
                        Contact Info: {new_item.contact_info}
                        
                        {candidate_footer}
                        """
                        send_mail(
                            subject_other,
                            message_other,
                            settings.EMAIL_HOST_USER,
                            [candidate.user.email], 
                            fail_silently=False,
                        )
                        print(f"   -> Notification sent to Previous User ({candidate.item_type})")
                    
                    print("--------------------------------------------------")
            
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/report_item.html', {'form': form})

def signup_view(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'items/signup.html', {'form': form})

@login_required
def my_reports(request):
    """Displays a list of items reported by the currently logged-in user."""
    items = Item.objects.filter(user=request.user).order_by('-date_reported')
    return render(request, 'items/my_reports.html', {'items': items})

@login_required
def delete_item(request, item_id):
    """Allows a user to delete their own report."""
    item = get_object_or_404(Item, id=item_id)
    if item.user == request.user:
        item.delete()
    return redirect('my_reports')

@login_required
def edit_item(request, item_id):
    """Shows the form to edit an existing item."""
    item = get_object_or_404(Item, id=item_id, user=request.user)
    form = ItemForm(instance=item)
    return render(request, 'items/edit_item.html', {'form': form, 'item': item})

@login_required
def update_item(request, item_id):
    """Handles the logic to update an item."""
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_reports')
    return redirect('edit_item', item_id=item.id)

@login_required
def item_detail(request, item_id):
    """Shows item details and suggests AI matches."""
    item = get_object_or_404(Item, id=item_id)
    
    # 1. Determine target type (Lost -> looks for Found)
    target_type = 'Found' if item.item_type == 'Lost' else 'Lost'
    
    # 2. Get candidates
    candidates = Item.objects.filter(item_type=target_type)
    
    matches = []
    
    # 3. AI Fuzzy Matching
    for candidate in candidates:
        name_score = fuzz.partial_ratio(item.name.lower(), candidate.name.lower())
        desc_score = fuzz.token_set_ratio(item.description.lower(), candidate.description.lower())
        
        avg_score = (name_score + desc_score) / 2
        
        if avg_score > 50:
            matches.append({
                'item': candidate,
                'score': int(avg_score)
            })
    
    matches.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'items/item_detail.html', {'item': item, 'matches': matches})
