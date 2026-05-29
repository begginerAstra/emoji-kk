import os
import difflib
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

# ============================================================
# EMOJIS PERSONALIZADOS
# Funciona com emoji estatico <:nome:id> e animado <a:nome:id>
# ============================================================

EMOJIS = {
    "crown": "<a:7130_kscrown:1509838833745657917>",
    "june_star": "<:8_june_star:1509838840842424390>",
    "announcements": "<:announcements:1509838804209369101>",
    "avisos": "<:avisos:1509838816704200794>",
    "badge": "<:BadgeBloxxer:1509835942511251526>",
    "blue_diamond": "<a:blue_diamond:1509838829601816666>",
    "caixa": "<:caixa:1509838858269753346>",
    "cashbag": "<:cashbagwhite:1509835839952261155>",
    "challenge": "<:Challenge:1489308367875735706>",
    "check": "<:Check:1509838811213991957>",
    "clock": "<:clock:1509838855300452434>",
    "vip": "<:daddy_VIP:1509838823926927381>",
    "cloudflare": "<:ducky_cloudflare:1509838838493745264>",
    "emoji53": "<:emoji_53:1509838818935701565>",
    "blue_fire": "<a:fogo_azul:1509838836237336616>",
    "giveaway": "<:giveaway:1509836081263280150>",
    "loading": "<a:loading:1509838825264775272>",
    "members": "<:members:1509838843065536643>",
    "neysi": "<a:Neysi:1509834396881125466>",
    "person": "<:Person:1509834083767816212>",
    "premium": "<:premium:1509838821435375659>",
    "gift": "<:RWE_gift:1509835468877988010>",
    "arrow": "<:seta_omg:1509838828100387048>",
    "shield": "<:shield:1509838851969908749>",
    "staff": "<:staff:1509838809280548946>",
    "store": "<:store:1509835369573777449>",
    "ticket": "<:ticket:1509836161005391882>",
    "ticket_alt": "<:Ticket:1509838806763835453>",
    "trophy": "<:trophy_v2:1509835283363926046>",
    "upvote": "<:upvote:1509835155374608404>",
    "x": "<:X_:1509838813487300618>",
    "coin": "<a:y_coin:1509833960463663147>",
}

TARGETS = {
    "MOEDA": ["moeda", "coin", "coins", "money", "cash", "y_coin"],
    "PERFIL": ["perfil", "profile", "person", "user", "membro"],
    "XP": ["xp", "exp", "experience"],
    "LEVEL": ["level", "lvl", "rankup"],
    "RANKING": ["ranking", "rank", "trophy", "trofeu", "leaderboard"],
    "LOJA": ["loja", "store", "shop"],
    "PRESENTE": ["presente", "gift", "recompensa", "reward"],
    "INVENTARIO": ["inventario", "inventory", "bag", "backpack"],
    "BADGE": ["badge", "badges", "star", "estrela"],
    "ANUNCIO": ["anuncio", "announce", "announcement", "announcements", "megafone"],
    "SORTEIO": ["sorteio", "giveaway", "party", "party_blob"],
    "TICKET": ["ticket", "suporte", "support"],
    "STAFF": ["staff", "mod", "admin", "equipe"],
    "SUCESSO": ["sucesso", "success", "check", "certo", "approved"],
    "ERRO": ["erro", "error", "errado", "x", "denied"],
    "AVISO": ["aviso", "warn", "warning", "alerta"],
    "CONFIG": ["config", "settings", "gear", "engrenagem"],
    "PREMIUM": ["premium", "pro", "plus"],
    "VIP": ["vip"],
    "LOADING": ["loading", "load", "carregando"],
    "SETA": ["seta", "arrow", "right", "left"],
    "DIAMANTE": ["diamante", "diamond", "gem"],
    "COROA": ["coroa", "crown", "king"],
    "FOGO": ["fogo", "fire", "flame"],
    "RAIO": ["raio", "bolt", "zap", "thunder"],
    "ESTRELA": ["estrela", "star"],
    "MEMBRO": ["membro", "member", "user", "person"],
    "ESCUDO": ["escudo", "shield", "security"],
    "GRAFICO": ["grafico", "chart", "stats", "graph"],
    "CAIXA": ["caixa", "box", "crate", "package"],
    "CARTEIRA": ["carteira", "wallet", "bank"],
    "DAILY": ["daily", "diario", "calendar", "gift"],
    "TRABALHAR": ["trabalhar", "work", "job", "briefcase"],
    "EDITAR": ["editar", "edit", "pen", "pencil"],
    "TEMPO": ["tempo", "time", "clock"],
    "CALENDARIO": ["calendario", "calendar", "date"],
    "BIO": ["bio", "about", "description"],
    "BANNER": ["banner", "background", "bg"],
    "SHOPPING_CART": ["cart", "carrinho", "shopping"],
    "CHECK": ["check", "confirm", "yes", "certo"],
    "X": ["x", "no", "cancel", "close"],
    "INFO": ["info", "information", "help"],
}

COLOR_DARK = 0x111111
COLOR_BLUE = 0x2F6FFF
COLOR_GREEN = 0x2ECC71
COLOR_GOLD = 0xF1C40F

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


def normalize(text: str) -> str:
    return text.lower().replace("_", "").replace("-", "").replace(" ", "")


def emoji_text(emoji: discord.Emoji) -> str:
    prefix = "a" if emoji.animated else ""
    return f"<{prefix}:{emoji.name}:{emoji.id}>"


def find_best(guild: discord.Guild, words: list[str]) -> discord.Emoji | None:
    emojis = list(guild.emojis)
    if not emojis:
        return None

    normalized_emojis = [(e, normalize(e.name)) for e in emojis]
    keys = [normalize(w) for w in words]

    for key in keys:
        for emoji, name in normalized_emojis:
            if name == key:
                return emoji

    for key in keys:
        for emoji, name in normalized_emojis:
            if key in name or name in key:
                return emoji

    best = None
    best_score = 0
    for emoji, name in normalized_emojis:
        for key in keys:
            score = difflib.SequenceMatcher(None, name, key).ratio()
            if score > best_score:
                best_score = score
                best = emoji

    return best if best_score >= 0.55 else None


async def send_lines(ctx: commands.Context, lines: list[str]):
    chunk = []
    size = 0

    for line in lines:
        if size + len(line) + 1 > 1700:
            await ctx.send("```txt\n" + "\n".join(chunk) + "\n```")
            chunk = []
            size = 0

        chunk.append(line)
        size += len(line) + 1

    if chunk:
        await ctx.send("```txt\n" + "\n".join(chunk) + "\n```")


def make_panel_embed() -> discord.Embed:
    embed = discord.Embed(
        title=f"{EMOJIS['crown']} Astra Community",
        description=(
            f"{EMOJIS['blue_fire']} **Bem-vindo ao painel principal.**\n\n"
            f"{EMOJIS['arrow']} Use os botões abaixo para navegar.\n"
            f"{EMOJIS['shield']} Sistema visual usando emojis estáticos e animados.\n"
            f"{EMOJIS['premium']} Layout limpo, escuro e profissional."
        ),
        color=COLOR_DARK,
    )

    embed.add_field(
        name=f"{EMOJIS['staff']} Staff",
        value=(
            f"{EMOJIS['check']} Suporte organizado\n"
            f"{EMOJIS['clock']} Atendimento rápido\n"
            f"{EMOJIS['avisos']} Avisos importantes"
        ),
        inline=True,
    )

    embed.add_field(
        name=f"{EMOJIS['ticket']} Tickets",
        value=(
            f"{EMOJIS['caixa']} Abrir atendimento\n"
            f"{EMOJIS['person']} Falar com equipe\n"
            f"{EMOJIS['x']} Fechar solicitação"
        ),
        inline=True,
    )

    embed.add_field(
        name=f"{EMOJIS['store']} Loja",
        value=(
            f"{EMOJIS['coin']} Moedas e vantagens\n"
            f"{EMOJIS['cashbag']} Compras seguras\n"
            f"{EMOJIS['gift']} Recompensas"
        ),
        inline=True,
    )

    embed.set_footer(text="Astra • Demo de painel com emojis personalizados")
    return embed


def make_ticket_embed(user: discord.abc.User) -> discord.Embed:
    embed = discord.Embed(
        title=f"{EMOJIS['ticket']} Ticket criado",
        description=(
            f"{EMOJIS['check']} Olá, {user.mention}. Seu ticket foi aberto com sucesso.\n\n"
            f"{EMOJIS['staff']} Aguarde um membro da equipe responder.\n"
            f"{EMOJIS['clock']} Evite marcar a staff várias vezes."
        ),
        color=COLOR_BLUE,
    )
    embed.set_footer(text="Sistema de tickets • Demo")
    return embed


class DemoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.primary, custom_id="astra_demo_ticket", emoji="🎫")
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=make_ticket_embed(interaction.user), ephemeral=True)

    @discord.ui.button(label="Loja", style=discord.ButtonStyle.secondary, custom_id="astra_demo_store", emoji="🛒")
    async def store_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=f"{EMOJIS['store']} Loja Astra",
            description=(
                f"{EMOJIS['coin']} **Saldo:** 0 moedas\n"
                f"{EMOJIS['premium']} **VIP:** Indisponível nesta demo\n"
                f"{EMOJIS['gift']} **Bônus:** Em breve"
            ),
            color=COLOR_GOLD,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Staff", style=discord.ButtonStyle.secondary, custom_id="astra_demo_staff", emoji="🛡️")
    async def staff_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=f"{EMOJIS['shield']} Área Staff",
            description=(
                f"{EMOJIS['staff']} Painel reservado para equipe.\n"
                f"{EMOJIS['announcements']} Aqui podem ficar logs, ações rápidas e avisos."
            ),
            color=COLOR_GREEN,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    bot.add_view(DemoView())

    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as exc:
        print(f"Erro ao sincronizar slash commands: {exc}")

    print(f"Bot online como {bot.user}")


@bot.command(name="emojis")
async def emojis_prefix(ctx: commands.Context):
    if not ctx.guild:
        await ctx.send("Use dentro do servidor que tem os emojis.")
        return

    emojis_list = sorted(ctx.guild.emojis, key=lambda e: e.name.lower())
    if not emojis_list:
        await ctx.send("Nenhum emoji customizado encontrado.")
        return

    lines = [f"{emoji_text(e)}  nome={e.name} id={e.id}" for e in emojis_list]
    await send_lines(ctx, lines)


@bot.command(name="mapear")
async def mapear(ctx: commands.Context):
    if not ctx.guild:
        await ctx.send("Use dentro do servidor que tem os emojis.")
        return

    lines = []
    for key, words in TARGETS.items():
        emoji = find_best(ctx.guild, words)
        if emoji:
            lines.append(f"{key}={emoji_text(emoji)}  nome={emoji.name} id={emoji.id}")
        else:
            lines.append(f"{key}=  nao_encontrei")

    await send_lines(ctx, lines)


@bot.command(name="ajuda")
async def ajuda(ctx: commands.Context):
    await ctx.send(
        "Comandos:\n"
        "`!emojis` lista todos os emojis do servidor.\n"
        "`!mapear` gera um mapeamento automatico.\n"
        "`!demo` envia o painel visual por comando de prefixo.\n"
        "Tambem existem os slash commands `/demo` e `/emoji_lista`."
    )


@bot.command(name="demo")
async def demo_prefix(ctx: commands.Context):
    await ctx.send(embed=make_panel_embed(), view=DemoView())


@bot.tree.command(name="demo", description="Envia uma demo visual usando os emojis personalizados.")
async def demo_slash(interaction: discord.Interaction):
    await interaction.response.send_message(content=f"{EMOJIS['loading']} Carregando painel...", ephemeral=True)
    await interaction.followup.send(embed=make_panel_embed(), view=DemoView(), ephemeral=False)


@bot.tree.command(name="emoji_lista", description="Mostra todos os emojis configurados no codigo da demo.")
async def emoji_lista(interaction: discord.Interaction):
    lines = [f"`{key}` {emoji}" for key, emoji in EMOJIS.items()]

    chunks = []
    atual = ""
    for line in lines:
        if len(atual) + len(line) + 1 > 3900:
            chunks.append(atual)
            atual = line
        else:
            atual += "\n" + line if atual else line

    if atual:
        chunks.append(atual)

    embed = discord.Embed(
        title=f"{EMOJIS['blue_diamond']} Emojis configurados",
        description=chunks[0],
        color=COLOR_DARK,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

    for extra in chunks[1:]:
        await interaction.followup.send(embed=discord.Embed(description=extra, color=COLOR_DARK), ephemeral=True)


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Configure DISCORD_TOKEN no Railway.")

    bot.run(TOKEN)
