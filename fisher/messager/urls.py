from django.urls import path
from fisher.messager import views


app_name = "messager"
urlpatterns = [
    path('', views.MessagesListView.as_view(), name='messages_list'),
    path('send-message/', views.send_message, name='send_message'),
    path('<username>/', views.ConversationListView.as_view(), name='conversation_detail'),
    # path('test_send_message/', views.test_message, name='test_send_message'),
]

