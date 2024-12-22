import discord
from discord.ext import commands
from discord import InteractionContextType, IntegrationType

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(  # 改用 discord.slash_command
        name="ping",
        description="檢查機器人延遲",
        integration_types=[  # 改用列表而不是集合
            IntegrationType.guild_install,
            IntegrationType.user_install
        ],
        contexts=[  # 改用列表而不是集合
            InteractionContextType.guild,
            InteractionContextType.private_channel,
            InteractionContextType.bot_dm
        ]
    )
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Ping 結果",
            description=f"機器人的延遲為 {self.bot.latency * 1000:.2f} 毫秒",
            color=discord.Color.blue()
        )
        embed.set_footer(text="由 py-cord 機器人提供")
        embed.timestamp = discord.utils.utcnow()

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(PingCog(bot))