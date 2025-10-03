from django.shortcuts import redirect, render
from blog.models import Users
from .models import Chat_list, Chat_message

# Create your views here.
def chatList(request):
    current_user = Users.objects.get(id=request.session.get('user_id'))
    user_chats = Chat_list.objects.filter(users=current_user)
    
    # Prepare chat data with other_user and last_message
    chats_data = []
    for chat in user_chats:
        other_user = chat.users.exclude(id=current_user.id).first()
        last_message = Chat_message.objects.filter(chat_id=chat).order_by('-timestamp').first()
        unread_count = 0  # You can implement unread message logic later
        
        chat_data = {
            'id': chat.id,
            'other_user': other_user,
            'last_message': last_message,
            'unread_count': unread_count
        }
        chats_data.append(chat_data)
    
    return render(request, 'chats/chatList.html', {'chats': chats_data, 'user': current_user})

def createConversation(request, user_id):
    user1 = Users.objects.get(id=request.session.get('user_id'))
    user2 = Users.objects.get(id=user_id)
    existing_chat = Chat_list.objects.filter(users=user1).filter(users=user2).first()
    if not existing_chat:
        chat = Chat_list.objects.create()
        chat.users.add(user1, user2)
        chat.save()
        return redirect('conversationView', chat_id=chat.id)
    else:
        return redirect('conversationView', chat_id=existing_chat.id)


def conversationView(request, chat_id):
    current_user = Users.objects.get(id=request.session.get('user_id'))
    chat = Chat_list.objects.get(id=chat_id)
    other_user = chat.users.exclude(id=current_user.id).first()
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        message = Chat_message.objects.create(chat_id=chat, message=message_text, sender=current_user)
        message.save()
        return redirect('conversationView', chat_id=chat_id)
    
    messages = Chat_message.objects.filter(chat_id=chat_id).order_by('timestamp')
    all_chats = Chat_list.objects.filter(users=current_user)
    return render(request, 'chats/conversation.html', {
        'chat_id': chat_id, 
        'messages': messages, 
        'user': current_user,
        'other_user': other_user,
        'chats': all_chats
    })