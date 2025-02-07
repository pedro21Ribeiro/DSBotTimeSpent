import discord
from discord.ext import commands
from database import SessionLocal, init_db
from models import UserActivity
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

init_db()

description = '''Meu primeiro bot clean de teste

Não sei direito o que eu estou fazendo mas quero aprender'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

EntSai = {}



@bot.event
async def on_ready():
    print(f"Logado como {bot.user} (id: {bot.user.id})")
    print('---------------------')

@bot.event
async def  on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel != None:
        hours = datetime.now().hour + datetime.now().minute / 60
        tempoDeCall = hours - EntSai[str(member.id)]
        print(f"{member.name} ficou na call {before.channel.name} por {tempoDeCall} horas")
        if(tempoDeCall >= 0.5):
            db = SessionLocal()
            try:
                existing_entry = db.query(UserActivity).filter(
                    UserActivity.member_id == str(member.id),
                    UserActivity.channel_id == str(before.channel.id)
                ).first()

                if existing_entry:
                    existing_entry.time += tempoDeCall
                    db.commit()
                else:
                    new_activity = UserActivity(
                        member_id=str(member.id),
                        channel_id=str(before.channel.id),
                        time=tempoDeCall
                    )
                    db.add(new_activity)
                    db.commit()
            except Exception as e:
                db.rollback()
                await bot.get_channel(879856877209530462).send(f"Houe um erro: {str(e)}")
            finally:
                db.close()
            pass #lógica para adicionar esse tempo ao tempo já no SQL
    
    if after.channel != None:
        print(f"Usuario {member.name} entrou na call {after.channel.name} as {datetime.now()}")
        hours = datetime.now().hour + datetime.now().minute / 60
        EntSai[str(member.id)] = hours 

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def entrou(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} entrou {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def mova(ctx, membro1: discord.Member, canal: discord.VoiceChannel = None):
    '''Troca o canal de alguém'''
    if(canal==None):
        await ctx.send("Canal é um argumento obrigatório")
        return

    await membro1.move_to(canal)

@bot.command(name="TopCanais")
async def top_channels(ctx, member: discord.Member):
    db = SessionLocal()
    try:
        # Query top 5 channels for the member
        channels = db.query(UserActivity).filter(
            UserActivity.member_id == str(member.id)
        ).order_by(UserActivity.time.desc()).limit(5).all()

        if not channels:
            await ctx.send(f"Não há dados para {member.name}.")
            return

        # Format response
        response = [f"**Top 5 canais de voz que {member.name} usou:**"]
        for idx, entry in enumerate(channels, 1):
            channel_id = entry.channel_id
            response.append(f"{idx}. <#{channel_id}> - {entry.time} horas")

        await ctx.send("\n".join(response))

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
    finally:
        db.close()

@bot.command(name="TopMembros")
async def top_users(ctx, channel: discord.VoiceChannel):
    db = SessionLocal()
    try:
        # Query top 5 users in the channel
        users = db.query(UserActivity).filter(
            UserActivity.channel_id == str(channel.id)
        ).order_by(UserActivity.time.desc()).limit(5).all()

        if not users:
            await ctx.send(f"Não há dados para o canal <#{channel.id}>.")
            return

        # Format response
        response = [f"**Top 5 membros no canal de voz <#{channel.id}>:**"]
        for idx, entry in enumerate(users, 1):
            member_id = entry.member_id
            response.append(f"{idx}. {bot.get_user(int(member_id))} - {entry.time} horas")

        await ctx.send("\n".join(response))

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
    finally:
        db.close()

@bot.command(name="TempoGasto")
async def user_channel_time(ctx, member: discord.Member, channel: discord.VoiceChannel):
    db = SessionLocal()
    try:
        # Query the specific user-channel entry
        entry = db.query(UserActivity).filter(
            UserActivity.member_id == str(member.id),
            UserActivity.channel_id == str(channel.id)
        ).first()

        if entry:
            await ctx.send(
                f"Usuario {member.name} gastou **{entry.time} horas** no <#{channel.id}>."
            )
        else:
            await ctx.send(f"Não há dados para o usuario {member.name} no canal <#{channel.id}>.")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
    finally:
        db.close()

@bot.command()
async def transmit(ctx, channel_id: int, *message: str):
    await bot.get_channel(channel_id).send(" ".join(message))

bot.run(os.getenv("DISCORD_TOKEN"))