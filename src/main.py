import httpx
import json
import asyncio
import pandas as pd
from loguru import logger
from io import StringIO
from dataclasses import dataclass
from tqdm import tqdm


@dataclass
class Config:
    group_url: str
    player_url: str
    refresh_interval: int
    player_throttle: int

def parse_config() -> Config:
    file = "src/config.json"
    with open(file, "r") as f:
        data = json.load(f)
    
    group_url: str = str(data["base_url_group"]).replace("!", str(data["group_id"]))
    player_url: str = data["base_url_player"]
    refresh_interval: int = data["interval_group"]
    player_throttle: int = data["interval_player"]
    return Config(group_url=group_url, player_url=player_url, refresh_interval=refresh_interval, player_throttle=player_throttle)

CONFIG = parse_config()
client = httpx.Client(headers={"User-Agent": "Clan Updater (4s per user, 3600s cooldown) SaltisRS on GH"})
bar_format = "{l_bar}{bar} | {n_fmt}/{total_fmt} [{elapsed} - {remaining} {rate_fmt}]"

async def handle_ratelimit(response):
    if response.status_code == 429:
        logger.error("\nRatelimited, Retrying in 5 Seconds.")
        await asyncio.sleep(5)
        return True
    return False
 
async def fetch_players():
    logger.info("Fetching Updated Player List...")
    response = client.get(CONFIG.group_url, timeout=30)
    if response.status_code == 200:
        csv = StringIO(response.text)
        df = pd.read_csv(csv)
        players = df.Player
        return players
    else:
        raise ConnectionError
        
async def update_players():
    try:
        players = await fetch_players()
    except ConnectionError:
        logger.error(f"Failed to fetch player data. Is wom down?, Retry in a bit.")
        exit(code="Connection Refused")
    await asyncio.sleep(2)
    pbar = tqdm(total=len(players), desc="WOM Updater", dynamic_ncols=True, unit="Member", bar_format=bar_format, colour="green")
    
    for player in players.tail(2):
        pbar.update(1)
        pbar.set_description(f"Updating: {player}")
        response = client.post(CONFIG.player_url + player, timeout=30)
        
        if await handle_ratelimit(response):
            response = client.post(CONFIG.player_url + player, timeout=30)
            if response.status_code != 200:
                logger.error(f"Could not update: {player} Status Code:{response.status_code}")
                await asyncio.sleep(CONFIG.player_throttle)
        
        else:
            await asyncio.sleep(CONFIG.player_throttle)
            
    
    pbar.close()
    logger.info(f"Session complete: Updated {len(players)}\nSleeping for: {CONFIG.refresh_interval / 60:.2f}min")
    await asyncio.sleep(CONFIG.refresh_interval)
            
        
        
async def main():
    while True:
        await update_players()
    
if __name__ == "__main__":
    asyncio.run(main())