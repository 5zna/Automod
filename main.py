import discord
from discord import app_commands
import aiohttp

TOKEN = "توكنك هنا يا خويي"
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.tree.command(name="automod", description="Create an AutoMod rule to block bad words.")
async def create_automod_rule(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)

    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }

    rule_data = {
        "name": "Block Swear Words",
        "event_type": 1,
        "trigger_type": 1,
        "trigger_metadata": {
            "keyword_filter": ["badword1", "badword2"]
        },
        "actions": [
            {
                "type": 1,
                "metadata": {}
            }
        ],
        "enabled": True,
        "exempt_roles": [],
        "exempt_channels": []
    }

    url = f"https://discord.com/api/v10/guilds/{guild_id}/auto-moderation/rules"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=rule_data) as resp:
            if resp.status in (200, 201):
                await interaction.response.send_message("✅ تم انشاء الامر للحصول على الشارة اكتب الامر فى ١٣ سيرفر حقيقى فيه اعضاء!", ephemeral=True)
            else:
                error_text = await resp.text()
                await interaction.response.send_message(
                    f"❌ فشل انشاء الاوتومود. Status: {resp.status}, Error: {error_text}",
                    ephemeral=True
                )

client.run(TOKEN)