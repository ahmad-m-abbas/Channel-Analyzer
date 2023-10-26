import discord
import json
import hashlib
from datetime import datetime

def hash_name(name):
    if name == None:
        return "None"
    return hashlib.md5(name.encode()).hexdigest()
    
TOKEN = ''

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

    channel = client.get_channel('')
    
    messages_data = []
    
    after_date = datetime(2018, 1, 1)

    i = 0
    async for message in channel.history(limit=None, after=after_date):
        print(i)
        i += 1
        try:
            reactions_data = [
                {
                    'emoji': {
                        'name': reaction.emoji.name if hasattr(reaction.emoji, 'name') else str(reaction.emoji),
                        'imageUrl': str(reaction.emoji.url) if hasattr(reaction.emoji, 'url') else None
                    },
                    'count': reaction.count
                }
                for reaction in message.reactions
            ]
        except Exception as e:
            print(f"Error processing reactions for message {message.id}: {e}")
            reactions_data = []
        
        name = ''
        if message.author.global_name is None or message.author.global_name == '':
            name = message.author.global_name
        message_data = {
            'type': str(message.type),
            'timestamp': message.created_at.isoformat(),
            'timestampEdited': message.edited_at.isoformat() if message.edited_at else None,
            'isPinned': message.pinned,
            'content': message.content,
            'author': {
                'id': str(message.author.id),
                'name': hash_name(name), 
                'nickname': hash_name(message.author.name), 
                'isBot': message.author.bot,
                'avatarUrl': str(message.author.avatar) 
            },
            'attachments': [{'url': attachment.url, 'filename': attachment.filename} for attachment in message.attachments],
            'embeds': [{'title': embed.title, 'description': embed.description, 'url': embed.url} for embed in message.embeds],
            'reactions': reactions_data,
            'mentions': [{'id': str(mention.id), 'name': mention.global_name, 'nickname': mention.name, 'isBot': mention.bot, 'avatarUrl': str(mention.avatar)} for mention in message.mentions]
        }
        
        messages_data.append(message_data)
    
    with open('dad_jokes.json', 'w', encoding='utf-8') as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=4)
    
    print('Message data has been saved to messages_data.json')
    await client.close()

client.run(TOKEN)