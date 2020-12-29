# Libraries
import discord
import requests
import json

# Variables
TOKEN="[INSERT DISCORD BOT TOKEN HERE]"
API_URL="https://query2.finance.yahoo.com/v7/finance/quote?symbols="

# Command names
prefix = "$"
helloCmd = prefix + "hello"
stockCmd = prefix + "stock"
pingCmd = prefix + "ping"
helpCmd = prefix + "help"
authorCmd = prefix + "author"

# Define client
client = discord.Client()

# Get stock info
def get_stocks(stock_symbol):
	response = requests.get(API_URL + stock_symbol)
	json_data = json.loads(response.text)
	stocks = json_data["quoteResponse"]["result"]
	embed_list = []

	for stock in stocks:
		# Valid symbol
		if ("displayName" in stock.keys()):
			# Name and symbol
			display_name = stock["displayName"]
			symbol = stock["symbol"]
			short_name = stock["shortName"]
			embed=discord.Embed(title="{} ({})".format(display_name, symbol), description=short_name, color=0x0080ff)
			embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/chart-increasing_1f4c8.png")
			
			# Market price
			market_price = "%0.2f" % stock["regularMarketPrice"]
			currency = stock["currency"]
			embed.add_field(name="Market Price:", value="${} {}".format(market_price, currency), inline=False)		
			
			# Market change
			market_change = "%0.2f" % stock["regularMarketChange"]
			market_change_percent = "%0.2f" % stock["regularMarketChangePercent"]
			embed.add_field(name="Market Change:", value="${} ({}%)".format(market_change, market_change_percent), inline=False)
			
			# Market open price
			open_price = "%0.2f" % stock["regularMarketOpen"]
			embed.add_field(name="Market Open Price:", value="${} {}".format(open_price, currency), inline=False)
			
			# Day low and high
			day_low = "%0.2f" % stock["regularMarketDayLow"]
			day_high = "%0.2f" % stock["regularMarketDayHigh"]		
			embed.add_field(name="Day Low to High:", value="${} to ${} {}".format(day_low, day_high, currency), inline=False)
			
			# 52-week low and high
			year_low = "%0.2f" % stock["fiftyTwoWeekLow"]
			year_high = "%0.2f" % stock["fiftyTwoWeekHigh"]		
			embed.add_field(name="52-Week Low to High:", value="${} to ${} {}".format(year_low, year_high, currency), inline=False)
			
			# Append to embed
			embed_list.append(embed)
		
		# Invalid symbol
		else:
			embed=discord.Embed(title="Symbol: {}".format(stock_symbol), color=0x0080ff)
			embed.add_field(name="{} was not found!".format(stock_symbol), value="Is {} a valid stock symbol?".format(stock_symbol), inline=False)
			embed_list.append(embed)

	return embed_list

# On Ready Event
@client.event
async def on_ready():
	print('Logged in as: {0.user}\nBot is ready to go!'.format(client))

# On Message Event
@client.event
async def on_message(message):
	# Variables
	msgAuthor = message.author
	msgContent = message.content
	msgChannel = message.channel

	# Check if message is from the bot
	if msgAuthor == client.user:
		return
	
	# Hello command
	elif msgContent.startswith(helloCmd):
		await msgChannel.send("Hello traders!")
	
	# Stock command
	elif msgContent.startswith(stockCmd):
		userMsg = msgContent.split(stockCmd + " ", 1)
		if len(userMsg) > 1:
			stock_symbol = userMsg[1].upper()
			print("Symbol:", stock_symbol)
			stocks = get_stocks(stock_symbol)
			for stock in stocks:
				await msgChannel.send(embed=stock)
		else:
			await msgChannel.send("Please enter a stock symbol!\nExample: `{} TSLA`".format(stockCmd))
	
	# Ping command
	elif msgContent.startswith(pingCmd):
		await msgChannel.send("Ping: {}ms".format(round(client.latency * 1000)))

	# Help command
	elif msgContent.startswith(helpCmd):
		embed=discord.Embed(title="Welcome to Stock Bot!", description="Need help? Here are the commands!", color=0x0080ff)
		embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/information_2139.png")
		embed.add_field(name=helloCmd, value="Display the bot's greeting message.", inline=False)	
		embed.add_field(name=stockCmd + " [symbol]", value="Get stock data by providing a stock symbol.", inline=False)
		embed.add_field(name=stockCmd + " [symbol1],[symbol2], etc.", value="Get stock data by providing multiple stock symbols.", inline=False)
		embed.add_field(name=pingCmd, value="Get the current ping (in ms).", inline=False)
		embed.add_field(name=helpCmd, value="Open this help menu again.", inline=False)
		embed.add_field(name=authorCmd, value="Who developed this bot? Find out with this command!", inline=False)	
		await msgChannel.send(embed=embed)
	
	# Author command
	elif msgContent.startswith(authorCmd):
		embed=discord.Embed(title="Author: Jacky Ly", url="https://github.com/lyjacky11", description="Check out my GitHub for more projects!", color=0x0080ff)
		embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/memo_1f4dd.png")
		embed.add_field(name="Powered by:", value="Python & Google Cloud", inline=True)
		embed.set_footer(text="Let me know if you have any feedback! :)")
		await msgChannel.send(embed=embed)
	
	# Invalid commands
	elif msgContent.startswith(prefix):
		await msgChannel.send("Invalid stock bot command!\nPrefix is: `{}`".format(prefix))
	
	# Other messages
	else:
		return

# Run client
client.run(TOKEN)
