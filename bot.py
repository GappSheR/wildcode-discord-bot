import discord
from discord import app_commands
from discord.ext import commands
from mctools import RCONClient
import os

# Настройка намерений
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- ДАННЫЕ СЕРВЕРА ---
RCON_HOST = 'wildcode.go-srv.top'
RCON_PORT = 25575  # Убедись, что порт RCON на хостинге именно такой
RCON_PASSWORD = '140523@@Gg'

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Бот {bot.user} успешно запущен!')

# Команда /op
@bot.tree.command(name="op", description="Выдать права оператора игроку")
async def op_command(interaction: discord.Interaction, игрок: str):
    try:
        rcon = RCONClient(RCON_HOST, port=RCON_PORT)
        if rcon.login(RCON_PASSWORD):
            rcon.command(f'op {игрок}')
            rcon.stop()

            embed = discord.Embed(
                title="🛡️ Выдача прав оператора",
                description=f"Игрок **{игрок}** успешно получил оператора на сервере **WildCode**!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{игрок}?size=100&helm")
            embed.set_footer(text=f"Выдал: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Ошибка: Неверный RCON пароль.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Ошибка подключения к серверу: {e}")

# Команда /скин
@bot.tree.command(name="скин", description="Показать скин и аватарку игрока")
async def skin_command(interaction: discord.Interaction, игрок: str):
    embed = discord.Embed(
        title=f"👕 Скин игрока: {игрок}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=f"https://crafatar.com/avatars/{игрок}?size=150&helm")
    embed.set_image(url=f"https://crafatar.com/renders/body/{игрок}?scale=5&helm")
    
    await interaction.response.send_message(embed=embed)

# Запуск бота с твоим токеном
bot.run('MTU1NDMxMzg4NDE0NjYwNjEzMQ.Ga7vc8.HVrEXycW_HYfdz6PPSZAPBXXPzWLCmli-0_CXA')
