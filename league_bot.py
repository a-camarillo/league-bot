import discord
from discord.ext import commands
import league
import matplotlib.pyplot as plt
import seaborn as sns
import os

client = commands.Bot(command_prefix='?')
token = os.environ.get('DISCORD_TOKEN')

@client.event
async def on_ready():
    print('Bot is ready.')
 
@client.command()
async def rank(ctx, name, region='na1'):
    summoner = league.Summoner(name=name,region=region)
    tier, rank, lp = summoner.get_rank()
    await ctx.send(f'{summoner.name} is {tier} {rank}, {lp} LP')
@client.command()
async def stats(ctx, name, region='na1'):
    summoner = league.Summoner(name=name,region=region)
    avg_kills, avg_deaths, avg_assists, avg_gold  = summoner.get_stats()
    await ctx.send(f'Average Kills: {avg_kills}\nAverage Deaths: {avg_deaths}\nAverage Assists: {avg_assists}\nGold Average: {avg_gold}')
@client.command()
async def champs(ctx, name, region='na1'):
    summoner = league.Summoner(name=name,region=region)
    wins, champions = summoner.get_champs()
    sns.set()
    graph = sns.countplot(y=champions,hue=wins)
    plt.legend(('Loss','Win'))
    graph.figure.savefig('graph.png',bbox_inches='tight')
    await ctx.send(file=discord.File('graph.png'))
    os.remove('graph.png')


client.run(token)
