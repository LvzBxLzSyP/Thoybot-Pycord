import discord
from discord.ext import commands
import discord.utils
import os
import sys
import traceback
import logging
import json
import asyncio
from typing import List
from pathlib import Path

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DiscordBot')

def load_config() -> str:
    """載入設定檔並返回 Token"""
    config_path = Path('config.json')
    
    # 如果設定檔不存在，創建默認設定
    if not config_path.exists():
        default_config = {
            "token": "your_token_here"
        }
        config_path.write_text(
            json.dumps(default_config, indent=4),
            encoding='utf-8'
        )
        logger.warning('找不到設定檔，已創建默認設定檔 config.json')
        return None
    
    try:
        config = json.loads(config_path.read_text(encoding='utf-8'))
        return config.get('token')
    except Exception as e:
        logger.error(f'載入設定檔時發生錯誤: {str(e)}')
        return None

class Bot(discord.Bot):
    def __init__(self):
        # 設置 intents
        intents = discord.Intents.default()
        
        super().__init__(intents=intents)
        self.initial_extensions: List[str] = []
        self.logger = logger
        
    def load_all_cogs(self) -> None:
        """載入 cogs 資料夾中的所有擴展"""
        try:
            # 確保 cogs 資料夾存在
            if not os.path.exists('./cogs'):
                os.makedirs('./cogs')
                self.logger.warning('找不到 cogs 資料夾，已自動創建')
                return

            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    cog_name = f'cogs.{filename[:-3]}'
                    self.initial_extensions.append(cog_name)
                    
        except Exception as e:
            self.logger.error(f'載入 Cogs 時發生錯誤: {str(e)}')
            traceback.print_exc()
        
    async def on_ready(self):
        """機器人啟動時的初始化設置"""
        self.load_all_cogs()
        
        for ext in self.initial_extensions:
            try:
                self.load_extension(ext)
                self.logger.info(f"成功載入擴展：{ext}")
            except Exception as e:
                self.logger.error(f"載入擴展 {ext} 時出錯：{str(e)}")
                traceback.print_exc()

        """機器人就緒時的處理"""
        try:
            # 同步斜線命令
            self.logger.info("正在同步斜線命令...")
            await self.sync_commands()
            
            # 設置機器人狀態
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.playing,
                    name="準備就緒！"
                )
            )
            
            self.logger.info(f'{self.user} 已上線')
            self.logger.info(f'延遲：{self.latency * 1000:.2f}ms')
            self.logger.info(f'已加入 {len(self.guilds)} 個伺服器')
            
        except Exception as e:
            self.logger.error(f'機器人初始化時發生錯誤: {str(e)}')
            traceback.print_exc()

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """處理錯誤事件"""
        self.logger.error(f'事件 {event} 發生錯誤')
        traceback.print_exc()

def main():
    """主程式入口"""
    # 載入 Token
    token = load_config()
    
    if not token or token == 'your_token_here':
        logger.error('請在 config.json 中設置有效的 Discord Token')
        sys.exit(1)

    bot = Bot()
    
    try:
        logger.info('正在啟動機器人...')
        bot.run(token)
    except discord.LoginFailure:
        logger.error('Token 無效，請檢查 Discord Token 是否正確')
    except Exception as e:
        logger.error(f'啟動機器人時發生錯誤: {str(e)}')
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())