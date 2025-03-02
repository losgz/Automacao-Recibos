import discord
from discord.ext import commands
import sheets

# Enable all necessary intents
intents = discord.Intents.default()
intents.messages = True  # Needed to detect messages
intents.message_content = True  # Required for bots that read messages

# Initialize the bot with the correct prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

ACTIONS = [
    "Funcionamento",
    "Atividades Formativas",
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
    "Alojamento",
    "Transportes",
    "Seguros",
    "Outros",
]

DOC_TYPE = [
    "Ato Único",
    "Estrangeiro",
    "Fatura",
    "Fatura-Recibo",
    "Recibo-Verde"
]

# Dictionary to track forms per user
receipt_sessions = {}

class Receipt:
    def __init__(self, user_id):
        self.user_id = user_id
        self.data = {}
        self.form_step = 1

    async def rec_form(self, ctx):
        """Handles the form process step-by-step."""
        match self.form_step:
            case 1:
                await actions(ctx)
                await ctx.send("Insira o número da ação correta.")

            case 2:
                await budget_areas(ctx)
                await ctx.send("Insira o número da área orçamental correta.")

            case 3:
                await doc_types(ctx)
                await ctx.send("Insira o número do tipo de documento.")

            case 4:
                await ctx.send("Insira o número.")

            case 5:
                await ctx.send("Insira a data.")

            case 6:
                await ctx.send("Insira o NIF.")

            case 7:
                await ctx.send("Insira o fornecedor.")

            case 8:
                await ctx.send("Insira a atividade.")
            
            case 9:
                await ctx.send("Insira a descrição.")

            case 10:
                await ctx.send("Insira o link.")

            case 11:
                await ctx.send("Insira o PAJ(y/N).")

            case 12:
                await ctx.send("Insira o RAC(y/N).")

            case _:
                await ctx.send("Formulário concluído!")
                await ctx.send(self.data)

                del receipt_sessions[self.user_id]  # Remove session
                
                sheet = sheets.Sheets()
                sheet.addEntry(self.data)
                del sheet

    async def handle_response(self, message):
        """Processes user responses for each form step."""
        try:
            match self.form_step:

                # Ações
                case 1:
                    choice = int(message.content)
                    if 0 <= choice < len(ACTIONS):
                        self.data["action"] = ACTIONS[choice]
                        self.form_step += 1
                        await message.channel.send(
                            f"Ação Escolhida: {self.data['action']}"
                        )
                        await self.rec_form(message.channel)
                    else:
                        await message.channel.send(
                            "Número inválido. Escolha um número da lista."
                        )

                # Área Orçamental
                case 2:
                    choice = int(message.content)
                    if 0 <= choice < len(AREAS):
                        self.data["area"] = AREAS[choice]
                        self.form_step += 1
                        await message.channel.send(
                            f"Área Orçamental Escolhida: {self.data['area']}"
                        )
                        await self.rec_form(message.channel)
                    else:
                        await message.channel.send(
                            "Número inválido. Escolha um número da lista."
                        )

                # Tipo de documento
                case 3:
                    choice = int(message.content)
                    if 0 <= choice < len(DOC_TYPE):
                        self.data["doc_type"] = DOC_TYPE[choice]
                        self.form_step += 1
                        await message.channel.send(
                            f"Tipo de Documento Escolhido: {self.data['doc_type']}"
                        )
                        await self.rec_form(message.channel)
                    else:
                        await message.channel.send(
                            "Número inválido. Escolha um número da lista."
                        )

                # Número
                case 4:
                    try:
                        num = int(message.content)
                        self.data["num"] = num
                        self.form_step += 1
                        await self.rec_form(message.channel)
                    except Exception:
                        await message.channel.send("Número inválido")

                # Data
                case 5:
                    try:
                        data = message.content.split("/")
                        assert 2020 <= int(data[0]) <= 2030 and len(data[0]) == 4
                        assert 1 <= int(data[1]) <= 12 and 1 <= len(data[1]) <= 2
                        assert 1 <= int(data[2]) <= 31 and 1 <= len(data[2]) <= 2
                        self.data["date"] = message.content
                        self.form_step += 1
                        await self.rec_form(message.channel)
                    except Exception:
                        await message.channel.send("Data inválida")

                # NIF
                case 6:
                    try:
                        num = int(message.content)
                        self.data["num"] = num
                        self.form_step += 1
                        await self.rec_form(message.channel)
                    except Exception:
                        await message.channel.send("NIF inválido")

                # Fornecedor
                case 7:
                    self.data["supplier"] = message.content
                    self.form_step += 1
                    await self.rec_form(message.channel)

                # Atividade
                case 8:
                    self.data["activity"] = message.content
                    self.form_step += 1
                    await self.rec_form(message.channel)

                # Descrição
                case 9:
                    self.data["descrição"] = message.content
                    self.form_step += 1
                    await self.rec_form(message.channel)

                # Link Fatura
                case 10:
                    self.data["link"] = message.content
                    self.form_step += 1
                    await self.rec_form(message.channel)

                # PAJ
                case 11:
                    check = True if message.content == "y" else False
                    self.data["paj"] = check
                    self.form_step += 1
                    await self.rec_form(message.channel)

                # RAC
                case 12:
                    check = True if message.content == "y" else False
                    self.data["rac"] = check
                    self.form_step += 1
                    await self.rec_form(message.channel)
                    
                    
        except ValueError:
            await message.channel.send("Por favor, insira um número válido.")


@bot.command()
async def actions(ctx):
    options = "\n".join([f"{i} - {action}" for i, action in enumerate(ACTIONS)])
    await ctx.send(f"**Escolha uma ação:**\n{options}")


@bot.command()
async def budget_areas(ctx):
    options = "\n".join([f"{i} - {area}" for i, area in enumerate(AREAS)])
    await ctx.send(f"**Escolha uma área orçamental:**\n{options}")


@bot.command()
async def doc_types(ctx):
    options = "\n".join([f"{i} - {doc_type}" for i, doc_type in enumerate(DOC_TYPE)])
    await ctx.send(f"**Escolha um tipo de documento:**\n{options}")


@bot.command()
async def form(ctx):
    """Starts the form for a user."""
    user_id = ctx.author.id
    if user_id in receipt_sessions:
        await ctx.send(
            "Já tens um formulário ativo. Completa-o antes de começar outro."
        )
        return

    receipt_sessions[user_id] = Receipt(user_id)
    await ctx.send("Iniciando o formulário... 🚀")
    await receipt_sessions[user_id].rec_form(ctx)


@bot.event
async def on_message(message):
    """Handles user responses when they are in an active form session."""
    if message.author == bot.user:
        return

    user_id = message.author.id
    if user_id in receipt_sessions:
        if not message.content.startswith(bot.command_prefix):
            await receipt_sessions[user_id].handle_response(message)
        else:
            await bot.process_commands(message)  # Ensures commands still work
    else:
        await bot.process_commands(message)  # Ensures commands still work


@bot.command()
async def reset(ctx):
    """Resets the form for the user"""
    user_id = ctx.author.id
    if user_id in receipt_sessions:
        del receipt_sessions[user_id]
        await ctx.send("Forms Resetado com sucesso! ✅")
    else:
        await ctx.send("Não existe um forms iniciado")


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

token = None
with open("keys/token.txt") as fin:
    token = fin.readline()

if token:
    bot.run(token)
else:
    raise ValueError("Invalid token")