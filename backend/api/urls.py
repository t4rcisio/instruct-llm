from django.urls import path
from .views import info, embeddingData, logs, getModels, chat, agent_chat

urlpatterns = [
    path('info', info, name='info'),
    path('embedding', embeddingData, name='embedding'),
    path('models', getModels, name='models'),
    path('chat', chat, name='chat'),
    path('agent', agent_chat, name='agent chat'),
    path('logs', logs, name='logs'),
]
