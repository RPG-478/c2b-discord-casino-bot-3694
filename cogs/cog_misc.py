from __future__ import annotations
import discord
from discord.ext import commands
from discord import app_commands

class CogMiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="casino_help", description="カジノBotのコマンド一覧と各ゲームのルールを表示します。")
    async def casino_help(self, interaction: discord.Interaction):
        """カジノBotの利用可能なコマンドとゲームルールを詳細に表示します。"""
        
        currency_name = "こいん"
        
        # ヘルプ表示用のEmbedを作成
        embed = discord.Embed(
            title="🎰 カジノBot ヘルプガイド",
            description=f"ようこそ、{interaction.guild.name}カジノへ！\nここでは、仮想通貨「{currency_name}」を使って様々なゲームを楽しめます。",
            color=discord.Color.gold()
        )
        
        # 1. 経済コマンド
        economy_commands = (
            f"**/balance** - 現在の所持金（{currency_name}）を確認します。\n"
            f"**/daily** - 1日1回、ボーナス{currency_name}を受け取ります。"
        )
        embed.add_field(name="💰 経済コマンド", value=economy_commands, inline=False)

        # 2. ギャンブルコマンド
        gambling_commands = (
            "**/slots [賭け金]** - スロットマシンに挑戦します。\n"
            "**/roulette [賭け金] [賭け方]** - ルーレットで数字や色に賭けます。\n"
            "**/blackjack [賭け金]** - ディーラー相手にブラックジャックをプレイします。\n"
            "**/chinchiro [賭け金]** - 3つのサイコロを使った日本の伝統的なゲーム、ちんちろをプレイします。"
        )
        embed.add_field(name="🎲 ギャンブルコマンド", value=gambling_commands, inline=False)
        
        # 3. ランキング/その他
        misc_commands = (
            "**/leaderboard** - 所持金が多いユーザーのランキングを表示します。\n"
            "**/casino_help** - このヘルプを表示します。"
        )
        embed.add_field(name="🏆 ランキング/その他", value=misc_commands, inline=False)

        # 4. ゲームルール概要
        rules_summary = (
            "**スロット (Slots)**: 3つのリールを回し、絵柄が揃うと配当が得られます。\n"
            "**ルーレット (Roulette)**: 0〜36の数字、または赤/黒/偶数/奇数などに賭けます。\n"
            "**ブラックジャック (Blackjack)**: カードの合計を21に近づけ、ディーラーより高い点数を目指します。21を超えるとバースト（負け）です。\n"
            "**ちんちろ (Chinchiro)**: 3つのサイコロを振り、役（例: ゾロ目、シゴロ）を作って勝負します。"
        )
        embed.add_field(name="📜 ゲームルール概要", value=rules_summary, inline=False)
        
        embed.set_footer(text="ゲームは自己責任で楽しみましょう！初期所持金は1000こいんです。")

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(CogMiscCog(bot))