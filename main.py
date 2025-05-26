import discord
import re
import asyncio
import time
from datetime import datetime, timedelta
from config import (
    EMOJI,
    COMMAND,
    VALID_USERS,
    MIN_KAKERA,
    MIN_KAKERA_LAST_HOUR,
    USER_TOKEN,
    SNIPE_TYPE,
    MUDAE_CHANNELS,
    ALL_CHANNELS
)

# this is mudae's ID. do not change
MUDAE = 432610292342587392

class automation(discord.Client):

    async def parse(self, msg: discord.Message):
        timestamp = time.strftime("%d %B %Y %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
        print(f"[{timestamp}] [{msg.channel}] PARSING: " + msg.content)
        if msg.content.startswith(f"<@{self.user.id}>") and "LIST DELAY" in msg.content.upper():
            now = time.time()
            for channel in self.mudae_channels:
                roll_delay = max(0, ((self.delays.get('roll') or {}).get(channel) or 0.01) - now)
                dailykakera_delay = max(0, ((self.delays.get('dailykakera') or {}).get(channel) or 0.01) - now)
                daily_delay = max(0, ((self.delays.get('daily') or {}).get(channel) or 0.01) - now)
                def fmt(t):
                    h = int(t) // 3600
                    m = (int(t) % 3600) // 60
                    s = t % 60
                    return f"{h}h {m}m {s:.3f}s"
                await msg.channel.send(
                    f"[{timestamp}] [{channel}] CURRENT DELAYS:\n"
                    f"ROLLS: {fmt(roll_delay)}\n"
                    f"DAILYKAKERA: {fmt(dailykakera_delay)}\n"
                    f"DAILY: {fmt(daily_delay)}"
                )
        if msg.content.startswith(f"<@{self.user.id}>") and "RUAN MEI" in msg.content.upper():
            await msg.channel.send("Yes honey?")
        if msg.content.startswith(f"<@{self.user.id}>") and "LIGMA" in msg.content.upper():
            command: discord.SlashCommand = next((cmd for cmd in await msg.channel.application_commands() if cmd.name == 'wa'), None)
            await command.__call__(channel=msg.channel)
            await msg.channel.send("AWAAA")
        if msg.content.startswith(f"<@{self.user.id}>") and "MAKE KAK" in msg.content.upper():
            await msg.channel.send("$mk")

    async def parse_mudae(self, msg: discord.Message):
        timestamp = time.strftime("%d %B %Y %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
        print(f"[{timestamp}] [{msg.channel}] PARSING FROM MUDAE: " + (msg.content if msg.content else "PARSING MUDAE CARD"))
        # character card
        if msg.embeds and (d := msg.embeds[0].to_dict()) and 'image' in d and 'author' in d and not d.get('footer', {}).get('text'):
            match SNIPE_TYPE:
                case 0:
                    b = (str(self.user.id) in msg.content and "Wished" in msg.content) # or msg.embeds[0].to_dict()['author']['name'] in WISHED
                case 1:
                    b = "Wished" in msg.content # or msg.embeds[0].to_dict()['author']['name'] in WISHED
                case _:
                    raise ValueError(f"INVALID SNIPE_TYPE: {SNIPE_TYPE}")
            if match:= re.search(r"\*\*(\d+)\*\*<:kakera:", msg.embeds[0].to_dict().get("description", "")):
                kakera = int(match.group(1))
            else:
                kakera = 0
            if b or kakera > MIN_KAKERA:
                # handle wish clicks
                await msg.add_reaction(EMOJI)
                if msg.components and msg.components[0].children:
                    await msg.components[0].children[0].click()
                print('------')
                print(f"[{timestamp}] [{msg.channel}] CLAIM ATTEMPTED ON: {msg.embeds[0].to_dict()['author']['name']} ({kakera} kakera)")
                print('------')  
            else:
                print(f"[{timestamp}] [{msg.channel}] SKIPPED {msg.embeds[0].to_dict()['author']['name']} ({kakera} kakera)")
        # claim successful
        if match := re.match(
            r'💖 \*\*' + re.escape(self.user.name) + 
            r'\*\* and \*\*(\w+)\*\* are now married! 💖',
            msg.content
        ):
            print('------')
            print(f"[{timestamp}] [{msg.channel}] SUCCESSFULLY CLAIMED: {match.group(1)}")
            print('------')
        # tu for time until next claim
        if match := re.match(
                r'^\*\*' + re.escape(self.user.name) + 
                r'\*\*, you (?:can\'t claim for another|__can__ claim right now! The next claim reset is in) '
                r'\*\*(?:(\d+)h )?(\d{1,2})\*\* min\.',
                msg.content
            ):
            self.next_claim[msg.channel] = time.time() + int(match.group(1) or 0) * 3600 + int(match.group(2)) * 60
            print('------')
            print(f"[{timestamp}] [{msg.channel}] TIME UNTIL NEXT CLAIM REFRESH: {int(match.group(1) or 0)} HOUR(S) {int(match.group(2))} MINUTES")
            print('------')
        # snipe restriction
        # kakera
        if msg.components and "kakera" in msg.components[0].children[0].emoji.name:
            print("kak detected")
            await msg.components[0].children[0].click()
        # roll wait / last hour claim
        if match := re.match(
                r'^\*\*' + re.escape(self.user.name) + r'\*\*, the roulette is limited to \d+ uses per hour\. \*\*(\d+)\*\* min left\.\n',
                msg.content):
            # last hour claim
            if MIN_KAKERA_LAST_HOUR > 0 and (self.next_claim.get(msg.channel) - time.time()) % (3 * 3600) < 3600:
                # check all character cards from last 42.5 seconds for kakera > MIN_KAKERA_LAST_HOUR
                async for message in msg.channel.history(after=(datetime.now() - timedelta(seconds=42.5))):
                    if message.author.id == MUDAE and message.embeds and (d := message.embeds[0].to_dict()) and 'image' in d and 'author' in d and not d.get('footer', {}).get('text'):
                        match SNIPE_TYPE:
                            case 0:
                                b = (str(self.user.id) in msg.content and "Wished" in msg.content)
                            case 1:
                                b = "Wished" in msg.content
                            case _:
                                raise ValueError(f"INVALID SNIPE_TYPE: {SNIPE_TYPE}")
                        if b or int(re.search(r"\*\*(\d+)\*\*<:kakera:", message.embeds[0].to_dict().get("description", "")).group(1)) > MIN_KAKERA_LAST_HOUR:
                            await message.add_reaction(EMOJI)
                            print('------')
                            print(f"[{timestamp}] [{msg.channel}] LAST HOUR CLAIM ATTEMPTED ON: {message.embeds[0].to_dict()['author']['name']}")
                            print('------')  
                            break
                        else:
                            print(f"[{timestamp}] [{msg.channel}] NO LAST HOUR CLAIM ATTEMPTED")
            # roll wait
            print('------')
            print(f"[{timestamp}] [{msg.channel}] PAUSING ROLLS FOR {match.group(1)} MINUTES ({int(match.group(1)) * 60 - 0.05 * int(match.group(1)) * 60} SECONDS)")
            print('------')
            self.loop.create_task(self.delay(int(match.group(1)) * 60 - 0.05 * int(match.group(1)) * 60, 'roll', msg.channel))
        # dailykakera wait
        if (match := re.fullmatch(
                r'^Next \$dk in \*\*(?:(\d+)h )?(\d{1,2})\*\* min\.$', msg.content.strip())
            ) and self.pause_dailykakera.get(msg.channel).is_set():
            print('------')
            print(f"[{timestamp}] [{msg.channel}] PAUSING $dailykakera FOR {match.group(1) if match.group(1) else 0} HOURS AND {match.group(2)} MINUTES")
            print('------')
            self.loop.create_task(self.delay(int(match.group(1) if match.group(1) else 0) * 3600 + int(match.group(2)) * 60 + 15, 'dailykakera', msg.channel))
        # daily wait
        if (match := re.match(
                r'^Next \$daily reset in \*\*(?:(\d+)h )?(\d{1,2})\*\* min\.',
                msg.content)) and self.pause_daily.get(msg.channel).is_set():
            print('------')
            print(f"[{timestamp}] [{msg.channel}] PAUSING $daily FOR {match.group(1) if match.group(1) else 0} HOURS AND {match.group(2)} MINUTES")
            print('------')
            self.loop.create_task(self.delay(int(match.group(1) if match.group(1) else 0) * 3600 + int(match.group(2)) * 60 + 15, 'daily', msg.channel))
        # daily wait without likelist
        if ((msg.content == 'Your Character likelist is empty: like characters with **$like** (or $l) then use this command every 20 hours to stack a rolls reset (usable with $rolls)') and
            self.pause_daily.get(msg.channel).is_set()):
            print('------')
            print(f"[{timestamp}] [{msg.channel}] PLEASE ADD 5 CHARACTERS TO YOUR LIKELIST IN ORDER FOR $daily TO WORK. PAUSING $daily FOR 20 HOURS")
            print('------')    
            self.loop.create_task(self.delay(20 * 3600, 'daily', msg.channel))

    async def delay(self, delay, type, channel):
        print("delaying")
        if type not in self.delays:
            self.delays[type] = {}
        self.delays[type][channel] = time.time() + delay
        match type:
            case 'roll':
                self.pause_roll.get(channel).clear()
                await asyncio.sleep(delay)
                self.pause_roll.get(channel).set()
            case 'dailykakera':
                self.pause_dailykakera.get(channel).clear()
                await asyncio.sleep(delay)
                self.pause_dailykakera.get(channel).set()
            case 'daily':
                self.pause_daily.get(channel).clear()
                await asyncio.sleep(delay)
                self.pause_daily.get(channel).set()
            case _:
                print("Unknown delay error at time " + time.strftime("%d %B %Y %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}")
        del(self.delays[type][channel])

    async def roll(self, channel):
        while not self.is_closed():
            await self.wait_until_ready()
            print("rolling")
            await self.pause_roll.get(channel).wait()
            await asyncio.sleep(2.5)
            await self.command.__call__(channel)
            await asyncio.sleep(5)
    async def dailykakera(self, channel):
        while not self.is_closed():
            await self.wait_until_ready()
            print("dailykakera-ing")
            await self.pause_dailykakera.get(channel).wait()
            await asyncio.sleep(5)
            await channel.send("$donkeykong")
            await asyncio.sleep(5)
    async def daily(self, channel):
        await self.wait_until_ready()
        while not self.is_closed():
            await self.pause_daily.get(channel).wait()
            await asyncio.sleep(7.5)
            await channel.send("$daily")
            await asyncio.sleep(5)
    async def listen_to_mudae(self):
        await self.wait_until_ready()
        while not self.is_closed():
            print("listening to mudae")
            try:
                await self.parse_mudae(await self.wait_for('message',timeout=10.0,
                                                                check=(lambda m: m.author.id == MUDAE and 
                                                                    m.channel in self.mudae_channels)))
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                with open("mudae_channels.log", "a") as f:
                    timestamp = time.strftime("%d %B %Y %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
                    f.write(f"[{timestamp}] MUDAE LISTENER CAUGHT A {type(e).__name__} - {str(e)}\n")
                continue
    async def listen(self):
        await self.wait_until_ready()
        while not self.is_closed():
            print("listening")
            try:
                await self.parse(await self.wait_for('message',timeout=10.0,
                                                            check=(lambda m: m.author.id in VALID_USERS and 
                                                                m.channel in self.all_channels)))
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                with open("all_channels.log", "a") as f:
                    timestamp = time.strftime("%d %B %Y %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
                    f.write(f"[{timestamp}] NON-MUDAE LISTENER CAUGHT A {type(e).__name__} - {str(e)}\n")
                continue

    async def mudae_init(self, channels):
        # $like a character for $daily to work
        await asyncio.gather(*(channel.send("$like ruan mei $ echidna $ albedo $ rias gremory $ makima") for channel in (channels if isinstance(channels, list) else [channels])))

    async def on_ready(self):
        # on_ready executes upon initial connection and ALL SUBSEQUENT RECONNECTIONS
        print(f'LOGGED IN AS {self.user} (ID: {self.user.id})')
        print('------')

        # terminate all existing tasks, delays, and other attributes
        all_tasks = []
        for task_type, channel_task_map in self.tasks.items():
            for channel, task in channel_task_map.items():
                if not task.done():
                    timestamp = time.strftime("%d %B %Y %H:%M:%S", time.localtime()) + f".{int(time.time() % 1 * 1000):03d}"
                    print(f"[{timestamp}] CANCELLING {task_type.upper()} TASK for CHANNEL {channel}")
                    task.cancel()
                all_tasks.append(task)
        await asyncio.gather(*all_tasks, return_exceptions=True)
        self.tasks.clear()
        self.delays.clear()
        self.next_claim.clear()
        
        # initialize channels
        self.mudae_channels = [ch for ch in (self.get_channel(cid) for cid in MUDAE_CHANNELS) if ch]
        self.all_channels = [ch for ch in (self.get_channel(cid) for cid in ALL_CHANNELS) if ch]
        if not self.mudae_channels or not self.all_channels:
            raise RuntimeError("ALL_CHANNELS OR MUDAE_CHANNELS EMPTY")
        self.command : discord.SlashCommand = next((cmd for cmd in await self.mudae_channels[0].application_commands() if cmd.name == COMMAND), None)

        # initialize tasks
        def new_event():
            e = asyncio.Event()
            e.set()
            return e
        self.pause_roll = dict(zip(self.mudae_channels, [new_event() for _ in self.mudae_channels]))
        self.pause_dailykakera = dict(zip(self.mudae_channels, [new_event() for _ in self.mudae_channels]))
        self.pause_daily = dict(zip(self.mudae_channels, [new_event() for _ in self.mudae_channels]))
        print(f"EVENTS INITIALIZED")
        print('------')

        # start listening
        self.tasks["listen_to_mudae"] = self.loop.create_task(self.listen_to_mudae())
        self.tasks["listen"] = self.loop.create_task(self.listen())
        
        # initialize settings
        await asyncio.gather(*(channel.send("$tu") for channel in self.mudae_channels))

        # start loops
        self.tasks["roll"] = dict(zip(self.mudae_channels, [self.loop.create_task(self.roll(channel)) for channel in self.mudae_channels]))
        self.tasks["dailykakera"] = dict(zip(self.mudae_channels, [self.loop.create_task(self.dailykakera(channel)) for channel in self.mudae_channels]))
        self.tasks["daily"] = dict(zip(self.mudae_channels, [self.loop.create_task(self.daily(channel)) for channel in self.mudae_channels]))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.tasks, self.delays, self.next_claim
        self.tasks = {}; self.delays = {}; self.next_claim = {}
        
automation(chunk_guilds_at_startup=False).run(str(USER_TOKEN))
