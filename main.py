import os
import difflib
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

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

intents = discord.Intents.default()
intents.message_content = True
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


async def send_lines(ctx, lines):
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


@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")


@bot.command(name="emojis")
async def emojis(ctx):
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
async def mapear(ctx):
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
async def ajuda(ctx):
    await ctx.send("Use `!emojis` para listar todos ou `!mapear` para gerar no formato do Astra Social.")


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Configure DISCORD_TOKEN no Railway.")
    bot.run(TOKEN)
