from __future__ import annotations
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import time
import datetime

# Constants for Casino Core operations
INITIAL_BALANCE = 1000
DAILY_BONUS = 200
COOLDOWN_SECONDS = 24 * 60 * 60

# NOTE: Data persistence (load/save) must utilize functions defined in utils/helpers.py
# We assume 'helpers' module is accessible and provides load_data/save_data.

class CasinoCore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Data access is delegated to external helper functions (helpers.load_data/save_data).

    def _get_user_data(self, data: dict, user_id: int) -> dict:
        """Ensures the user exists in the data structure and returns their entry, initializing if necessary."""
        user_id_str = str(user_id)
        if user_id_str not in data.get("users", {}):
            # Initialize new user with default balance (1000こいん)
            data.setdefault("users", {})[user_id_str] = {
                "balance": INITIAL_BALANCE,
                "last_daily": 0, # Unix timestamp
                "stats": {"total_wagered": 0, "total_won": 0}
            }
        return data["users"][user_id_str]

    @app_commands.command(name="balance", description="あなたの現在の所持こいんを確認します。他のユーザーを指定することも可能です。")
    async def balance(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        target_user = user or interaction.user
        
        # Load all user data from the JSON file
        data = await helpers.load_data()
        
        # Retrieve or initialize user data
        user_data = self._get_user_data(data, target_user.id)
        current_balance = user_data["balance"]
        
        embed = discord.Embed(
            title="💰 所持こいん残高",
            color=discord.Color.gold()
        )
        
        if target_user.id == interaction.user.id:
            embed.description = f"{target_user.mention} さんの現在の所持こいんです。"
        else:
            embed.description = f"{target_user.display_name} さんの現在の所持こいんです。"
            
        embed.add_field(name="残高", value=f"**{current_balance:,}** こいん", inline=True)
        embed.set_thumbnail(url=target_user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="24時間に1回、ボーナスとして200こいんを受け取ります。")
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        current_time = time.time()
        
        # Load user data
        data = await helpers.load_data()
        user_data = self._get_user_data(data, user_id)
        
        last_daily = user_data["last_daily"]
        
        # Check if 24 hours (COOLDOWN_SECONDS) have passed
        if current_time - last_daily >= COOLDOWN_SECONDS:
            # Grant daily bonus
            user_data["balance"] += DAILY_BONUS
            user_data["last_daily"] = current_time
            
            # Save updated data immediately
            await helpers.save_data(data)
            
            new_balance = user_data["balance"]
            
            embed = discord.Embed(
                title="✅ デイリーボーナス獲得！",
                description=f"ボーナスとして **{DAILY_BONUS} こいん** を受け取りました！",
                color=discord.Color.green()
            )
            embed.add_field(name="現在の残高", value=f"{new_balance:,} こいん", inline=False)
            embed.set_footer(text="次のデイリーボーナスは24時間後に受け取れます。")
            
            await interaction.response.send_message(embed=embed)
            
        else:
            # Cooldown is active
            time_remaining = last_daily + COOLDOWN_SECONDS - current_time
            
            # Calculate remaining time components and format as HH:MM:SS
            remaining_delta = datetime.timedelta(seconds=int(time_remaining))
            hours, remainder = divmod(remaining_delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            
            embed = discord.Embed(
                title="⏳ クールダウン中",
                description=f"デイリーボーナスはまだ受け取れません。",
                color=discord.Color.red()
            )
            embed.add_field(name="残り時間", value=time_str, inline=False)
            embed.set_footer(text="焦らず、また明日お越しください！")
            
            # Send ephemeral message so only the user sees the cooldown
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ranking", description="サーバー内の所持こいんランキングTOP10を表示します。")
    async def ranking(self, interaction: discord.Interaction):
        # Load ALL user data
        data = await helpers.load_data()
        
        users_data = data.get("users", {})

        if not users_data:
            await interaction.response.send_message("まだ誰もこいんを持っていません。", ephemeral=True)
            return

        # Extract users and their balances
        ranking_list = []
        for user_id_str, user_data in users_data.items():
            try:
                user_id = int(user_id_str)
                balance = user_data.get("balance", 0)
                # Only include users with a positive balance for ranking visibility
                if balance > 0:
                    ranking_list.append((user_id, balance))
            except ValueError:
                continue # Skip invalid user IDs
        
        # Sort by balance in descending order
        ranking_list.sort(key=lambda x: x[1], reverse=True)
        
        # Take the top 10
        top_10 = ranking_list[:10]
        
        embed = discord.Embed(
            title="🏆 こいん所持ランキング TOP 10",
            color=discord.Color.gold()
        )
        
        rank_display = []
        
        # Resolve user names asynchronously
        for rank, (user_id, balance) in enumerate(top_10, 1):
            user_name = f"ID: {user_id}"
            
            try:
                # Fetch the user object to get display name
                user = await self.bot.fetch_user(user_id)
                user_name = user.display_name
            except (discord.NotFound, discord.HTTPException):
                # Fallback if user cannot be fetched (e.g., left the server, API error)
                user_name = f"元ユーザー ({user_id})"
            
            # Determine emoji for top ranks
            if rank == 1:
                emoji = "🥇"
            elif rank == 2:
                emoji = "🥈"
            elif rank == 3:
                emoji = "🥉"
            else:
                emoji = f"{rank}."
                
            rank_display.append(f"{emoji} **{user_name}**: {balance:,} こいん")

        if rank_display:
            embed.description = "\n".join(rank_display)
        else:
            embed.description = "ランキング対象のユーザーがいません。"
            
        embed.set_footer(text=f"サーバー: {interaction.guild.name}")
        
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CasinoCore(bot))