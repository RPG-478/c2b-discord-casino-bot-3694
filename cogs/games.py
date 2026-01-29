import discord
from discord.ext import commands
from discord import app_commands
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # SECURITY FIX: Removed file I/O (open()) for persistence.
        # Using in-memory storage (dict) for game state instead.
        # Data will be reset upon bot restart.
        self.scores = {}

    @app_commands.command(name="roll", description="Rolls a standard six-sided die.")
    async def roll_die(self, interaction: discord.Interaction):
        """サイコロを振ります (1-6)"""
        
        # 応答遅延を防ぐため defer を使用
        await interaction.response.defer(thinking=True)
        
        result = random.randint(1, 6)
        
        user_id = str(interaction.user.id)
        
        # スコア更新 (インメモリ)
        self.scores[user_id] = self.scores.get(user_id, 0) + result
        current_score = self.scores[user_id]
        
        await interaction.followup.send(
            f"🎲 {interaction.user.mention} は **{result}** を出しました！ "
            f"現在の合計スコアは {current_score} です。"
        )

    @app_commands.command(name="score", description="Shows your current game score.")
    async def show_score(self, interaction: discord.Interaction):
        """現在のスコアを表示します"""
        user_id = str(interaction.user.id)
        current_score = self.scores.get(user_id, 0)
        
        await interaction.response.send_message(
            f"🏆 {interaction.user.mention} さんの現在のスコアは {current_score} です。",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Games(bot))