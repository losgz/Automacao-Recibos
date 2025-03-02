import discord
from discord.ext import commands

# Enable all necessary intents
intents = discord.Intents.default()
intents.messages = True  # Needed to detect messages
intents.message_content = True  # Required for bots that read messages

# Initialize the bot with the correct prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

ACTIONS = [
    "Funcionamento",
    "Ativiades Formativas",
    "Atividades Recreativas",
    "Relações Empresariais",
    "Merchandise",
    "ExtraPAJ",
    "NERD",
    "Ponto-socorro",
    "NAVEE",
    "Tech4Students",
]

AREAS = [
    "Alimentação",
    "Estrutura RH",
    "Estrutura Func",
    "Meios Téc e Mat",
    "Alimentação",
    "Alojamento",
    "Transporte",
    "Seguro",
    "Outros"
]

DOC_TYPE = ["Ato Único", "Estrangeiro", "Fatura", "Fatura-Recibo", "Recibo-Verde"]

class Receipt:
    def __init__(self):
        self.data = {}


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_message(message):
    print(
        f"📩 Received message: {message.content} from {message.author}"
    )  # Debugging log
    await bot.process_commands(message)  # Allow commands to be processed


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, human! 🤖")


# Run bot
bot.run("")
