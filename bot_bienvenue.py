import discord
from discord.ext import commands
from easy_pil import Editor, load_image, Font
import os

# --- CONFIGURATION (Utilise les variables d'environnement Railway) ---
TOKEN = os.getenv("DISCORD_TOKEN")
# L'ID du salon où envoyer l'image
ID_SALON_BIENVENUE = int(os.getenv("ID_SALON")) 

# IDs des rôles à donner à l'arrivée
ROLES_A_DONNER = [1426124058382307398, 1426124033887572011]

intents = discord.Intents.default()
intents.members = True  # Requis pour détecter les nouveaux membres et donner des rôles

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Le bot {bot.user.name} est en ligne et prêt sur Railway !')

@bot.event
async def on_member_join(member):
    # --- 1. ATTRIBUTION DES RÔLES ---
    try:
        roles = [member.guild.get_role(role_id) for role_id in ROLES_A_DONNER]
        # On filtre au cas où un ID de rôle serait incorrect
        roles = [role for role in roles if role is not None]
        
        if roles:
            await member.add_roles(*roles)
            print(f"Rôles attribués à {member.name}")
    except Exception as e:
        print(f"Erreur lors de l'attribution des rôles : {e}")

    # --- 2. CRÉATION DE L'IMAGE ---
    try:
        # Charger le fond (Assure-toi que content.jpg est sur ton GitHub)
        editor = Editor("content.jpg").resize((800, 500))
        
        # Préparer l'avatar
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        avatar_raw = load_image(str(avatar_url))
        avatar = Editor(avatar_raw).resize((180, 180)).circle_image()
        
        # Placement centré
        editor.paste(avatar, (310, 90))
        
        # Polices et Textes
        font_name = Font.poppins(size=45, variant="bold")
        font_msg = Font.poppins(size=30, variant="regular")

        editor.text((400, 300), f"{member.name}", color="white", font=font_name, align="center")
        editor.text((400, 370), "BIENVENUE SUR HTS", color="#A0C0FF", font=font_msg, align="center")

        # --- 3. ENVOI ---
        file = discord.File(fp=editor.image_bytes, filename="bienvenue.png")
        channel = bot.get_channel(ID_SALON_BIENVENUE)
        
        if channel:
            await channel.send(f"Bienvenue {member.mention} ! On t'a donné tes accès.", file=file)
            
    except Exception as e:
        print(f"Erreur lors de la création de l'image : {e}")

bot.run(TOKEN)
