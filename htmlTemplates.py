# css = '''
# <style>
# .chat-message {
#     padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
# }
# .chat-message.user {
#     background-color: #2b313e
# }
# .chat-message.bot {
#     background-color: #475063
# }
# .chat-message .avatar {
#   width: 20%;
# }
# .chat-message .avatar img {
#   max-width: 78px;
#   max-height: 78px;
#   border-radius: 50%;
#   object-fit: cover;
# }
# .chat-message .message {
#   width: 80%;
#   padding: 0 1.5rem;
#   color: #fff;
# }
# '''

# bot_template = '''
# <div class="chat-message bot">
#     <div class="avatar">
#         <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
#     </div>
#     <div class="message">{{MSG}}</div>
# </div>
# '''

# user_template = '''
# <div class="chat-message user">
#     <div class="avatar">
#         <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
#     </div>    
#     <div class="message">{{MSG}}</div>
# </div>
# '''


css = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

body {
    font-family: 'Roboto', sans-serif;
    background-color: #f0f2f5;
}

.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.chat-message {
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    animation: fadeIn 0.5s;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-message.user {
    background-color: #007bff;
    color: white;
    margin-left: 60px;
}

.chat-message.bot {
    background-color: #f8f9fa;
    color: #343a40;
    margin-right: 60px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.chat-message .avatar {
    width: 15%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-message .avatar img {
    max-width: 50px;
    max-height: 50px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 85%;
    padding: 0 1.5rem;
    line-height: 1.5;
}

.chat-message .message p {
    margin: 0;
}

.timestamp {
    font-size: 0.75rem;
    color: #6c757d;
    margin-top: 5px;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="message">
        {{MSG}}
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">
        {{MSG}}
</div>
'''

