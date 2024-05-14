from django.shortcuts import render

# Create your views here.

# from django.shortcuts import render, redirect
# from .forms import EmailTemplateForm, EmailCampaignForm
#
# def create_template(request):
#     if request.method == 'POST':
#         form = EmailTemplateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('templates_list')
#     else:
#         form = EmailTemplateForm()
#     return render(request, 'create_template.html', {'form': form})
#
# def create_campaign(request):
#     if request.method == 'POST':
#         form = EmailCampaignForm(request.POST)
#         if form.is_valid():
#             campaign = form.save()
#             campaign.send_emails()
#             return redirect('campaigns_list')
#     else:
#         form = EmailCampaignForm()
#     return render(request, 'create_campaign.html', {'form': form})
