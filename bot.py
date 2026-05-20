import json
import logging
from typing import Dict, Any, Optional
import tiktok
import proxies
import creator
import account

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TikTokBotManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
       
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Hata: '{self.config_path}' dosyası bulunamadı!")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Hata: '{self.config_path}' dosyası geçerli bir JSON formatında değil!")
            return {}

    def initialize_creator(self) -> None:
        """Hesap oluşturucu modülünü başlatır."""
        try:
            creator.init("tiktok.com", accounts=True)
            logger.info("Creator modülü başarıyla başlatıldı.")
        except Exception as e:
            logger.error(f"Creator başlatılırken hata oluştu: {e}")

    def create_account(self) -> Optional[Any]:
        """Yeni bir TikTok hesabı oluşturur ve profil ayarlarını yapar."""
        try:
            # Hesap olusturma kismo
            x = creator.newAccount(tiktok, account.email, account.password, account.username)
            if hasattr(x, 'append'):
                x.append()
            
            # Global tanımlı olduğunu varsaydığımız değişkenler (RandomPictureNet vb.)
            x.changeAvatar(RandomPictureNet)
            x.subTo(MostFolloweds)
            
            logger.info(f"Hesap başarıyla oluşturuldu: {account.username}")
            return x
        except Exception as e:
            logger.error(f"Hesap oluşturma sırasında kritik hata: {e}")
            return None

    def run_sub_bot(self, account_instance: Any) -> None:
        """Oluşturulan hesabın hedef hesabı takip etmesini sağlar."""
        if not account_instance:
            logger.warning("Geçersiz hesap nesnesi. İşlem iptal edildi.")
            return

        # Durum kontrolleri (-> işareti yerine temiz Python if-blokları)
        if getattr(account_instance, 'banned', False):
            logger.warning("İşlem başarısız: Hesap banlandi !")
            return

        if getattr(account_instance, 'doesNotExist', False):
            logger.info("Hesap mevcut değil, atlanıyor...")
            return

        try:
            target_account = self.config.get("acc")
            if not target_account:
                logger.error("JSON dosyasında 'acc' hedefi bulunamadı!")
                return            account_instance.subTo(target_account)          
            # Takipçi sayısını loglama
            current_followers = getattr(account_instance, 'followers', 0)
            logger.info(f"Takip başarılı! Güncel Takipçi: {current_followers + 1}")
            
        except Exception as e:
            logger.error(f"hata: {e}")



if __name__ == "__main__":
    
    bot = TikTokBotManager(config_path="config.json")
    bot.initialize_creator()
    
    # Yeni hesap oluşturuyoruz
    yeni_hesap = bot.create_account()
    
    # Eğer hesap duzgun olustuysa buna atiyor falan
    if yeni_hesap:
        bot.run_sub_bot(yeni_hesap)
