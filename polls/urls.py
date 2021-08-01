from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path('', views.index, name="index"),
    # Index of user polls, add new poll
    path('myIndex/',views.my_polls,name='my_index'),
    # Voting Page
    path('polls/votingPage/<str:poll_name>/',views.votingPage,name='voting_page'),
    path('polls/votingPage/<str:poll_name>/<str:preview>/',views.votingPage,name='voting_pagePreview'),

    # Get poll groups - javascript fetch api
    path('polls/getGroups/<str:poll_name>/',views.get_groups,name='getGroups'),
    # Get group categories - javascript fetch api
    path('polls/getCategories/<str:poll_name>/<str:group_name>/',views.get_categories,name='getCategories'),
    # Get category candidates - javascript fetch api
    path('polls/getCandidates/<str:poll_name>/<str:category_name>/',views.get_candidates,name='getCandidates'),
    # Vote - javascript fetch api
    path('polls/vote/<str:poll_name>/',views.vote,name='vote'),
    # Results
    path('polls/resultsIndex/',views.results_index,name='results_index'),
    path('polls/results/<str:poll_name>/',views.resultsPage,name='resultsPage'),
    path('polls/get_results/<str:poll_name>/<str:category_name>/<str:sort>/',views.results,name='results'),
    
    ## MANAGEING POLL(ADMIN/CREATOR)
    # Manage poll, add category, add candidate
    path('polls/manage/<str:poll_name>/<str:view>/',views.poll_management,name='poll_management'),

    # Get all categories
    path('polls/<str:poll_name>/management/categories/', views.manage_categories, name ="categories_management"),

    # Get all candidates
    path('polls/<str:poll_name>/management/candidates/', views.manage_candidates, name ="candidates_management"),

    # Manage settings
    path('polls/<str:poll_name>/management/settings/', views.manage_settings, name ="settings_management"),

    # Manage keys
    path('polls/<str:poll_name>/management/keys/', views.poll_keys, name ="keys_management"),

    # Keys Upload and Print(Excel)
    path('polls/<str:poll_name>/Excelkeys/', views.excel_keys, name ="keys_excel"),

     # Input Key
    path('polls/<str:poll_name>/inputKey/', views.input_key, name ="input_key")

]
