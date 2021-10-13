import discord
from discord.ext import commands, tasks

import simpledate
import calendar
import requests
import json


# GET NEWS To JSON FILE
def get_news():
    r = requests.get("https://nfs.faireconomy.media/ff_calendar_thisweek.json")
    json_file = r.json()
    # Filter python objects with list comprehensions
    output_dict = [x for x in json_file if (x['impact'] == 'High' or x['impact'] == 'Holiday')]
    # Transform python object back into json
    output_json = json.dumps(output_dict, sort_keys=True, indent=4)
    # Show json
    # print(output_json)
    return output_json


def discord_app():
    # Discord
    token = ""  # Here goes your bot token
    channel = 123456789  # Here goes the channel ID

    bot = commands.Bot("!")

    @tasks.loop(hours=24)
    async def called_once_a_day():
        message_channel = bot.get_channel(channel)
        print(f"Got channel {message_channel}")
        my_json = json.loads(get_news())
        embed = discord.Embed(title="This week news", description="", color=0x8877dd)
        separator = "═════════════════════════════════════"
        for item in my_json:
            # Date
            # London
            datetime = simpledate.SimpleDate(item['date']).convert(country='GB', tz='Europe/London')
            weekday = calendar.day_name[datetime.weekday]
            tz = str(datetime.time)[0:5] + ' (Europe/London)'
            date_ldn = f"{weekday} - {datetime.day} {calendar.month_abbr[datetime.month]}, {datetime.year}  {tz}"
            # NewYork
            datetime = simpledate.SimpleDate(item['date']).convert(country='US', tz='America/New_York')
            weekday = calendar.day_name[datetime.weekday]
            tz = str(datetime.time)[0:5] + ' (America/New_York)'
            date_nyc = f"{weekday} - {datetime.day} {calendar.month_abbr[datetime.month]}, {datetime.year}  {tz}"
            # Australia
            datetime = simpledate.SimpleDate(item['date']).convert(country='AU', tz='Australia/Sydney')
            weekday = calendar.day_name[datetime.weekday]
            tz = str(datetime.time)[0:5] + ' (Australia/Sydney)'
            date_aus = f"{weekday} - {datetime.day} {calendar.month_abbr[datetime.month]}, {datetime.year}  {tz}"

            # Impact
            impact = ""
            if item['impact'] == "High":
                impact = "🟥"
            elif item['impact'] == "Medium":
                impact = "🟧"
            elif item['impact'] == "Holiday":
                impact = "🌴"

            name = f"{separator}\n\n{impact} - {item['country']}"
            value = f"{item['title']}\n\n{date_ldn}\n{date_nyc}\n{date_aus}"
            # Adding field
            embed.add_field(name=name, value=value, inline=False)

        await message_channel.send(embed=embed)

    @called_once_a_day.before_loop
    async def before():
        await bot.wait_until_ready()
        print("Finished waiting")

    called_once_a_day.start()
    bot.run(token)


if __name__ == '__main__':
    discord_app()
