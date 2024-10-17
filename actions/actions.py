from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
from datetime import datetime
import pytz

class ActionHavaDurumu(Action):

    def name(self) -> Text:
        return "action_hava_durumu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sehir = tracker.get_slot("sehir")

        if not sehir:
            dispatcher.utter_message(template="utter_sor_hangi_sehir")
            return []

        duzeltilmis_sehir = sehir.lower().capitalize()

        api_key = "da8c497f530bea97455b28482b9df8db"
        base_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=tr&units=metric"
        url = base_url.format(duzeltilmis_sehir, api_key)
        response = requests.get(url).json()

        if response.get("cod") != 200:
            dispatcher.utter_message(text=f"Üzgünüm, {duzeltilmis_sehir} için hava durumu bilgisi alınamadı.")
            return []

        weather_info = response["weather"][0]["description"]
        temperature = response["main"]["temp"]
        country = response["sys"]["country"]
        weather_info_text = (f"{duzeltilmis_sehir} ({country}) için hava durumu: "
                             f"{weather_info}, "
                             f"sıcaklık: {temperature}°C")

        dispatcher.utter_message(text=weather_info_text)
        return [SlotSet("sehir", None)]  # Hava durumu bilgisinden sonra şehri sıfırla

def turkce_tarih_zamani_formatla(zaman_bilgisi: datetime) -> str:
    gunler = {
        'Monday': 'Pazartesi',
        'Tuesday': 'Salı',
        'Wednesday': 'Çarşamba',
        'Thursday': 'Perşembe',
        'Friday': 'Cuma',
        'Saturday': 'Cumartesi',
        'Sunday': 'Pazar'
    }

    aylar = {
        'January': 'Ocak',
        'February': 'Şubat',
        'March': 'Mart',
        'April': 'Nisan',
        'May': 'Mayıs',
        'June': 'Haziran',
        'July': 'Temmuz',
        'August': 'Ağustos',
        'September': 'Eylül',
        'October': 'Ekim',
        'November': 'Kasım',
        'December': 'Aralık'
    }

    gun = gunler[zaman_bilgisi.strftime("%A")]
    ay = aylar[zaman_bilgisi.strftime("%B")]
    tarih_bilgisi = zaman_bilgisi.strftime(f"%d {ay} %Y")
    saat_bilgisi = zaman_bilgisi.strftime("%H:%M")

    return f"{gun}, {tarih_bilgisi} ve saat {saat_bilgisi}"

class ActionTarihSaat(Action):

    def name(self) -> Text:
        return "action_tarih_saat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sehir = tracker.get_slot("sehir")  # Kullanıcıdan şehir bilgisi al
        try:
            if sehir:
                # Şehir için uygun saat dilimini al
                sehir_saat_dilimi = self.get_timezone_for_city(sehir)
                if not sehir_saat_dilimi:
                    raise ValueError("Bilinmeyen şehir")

                zaman_bilgisi = datetime.now(pytz.timezone(sehir_saat_dilimi))
                turkce_zaman = turkce_tarih_zamani_formatla(zaman_bilgisi)

                mesaj = f"{sehir.capitalize()} için bugün {turkce_zaman}."
                dispatcher.utter_message(text=mesaj)
                return [SlotSet("sehir", None)]  # Şehir slot'unu sıfırla
            else:
                # Şehir yoksa yerel saat ve tarih bilgisi göster
                kullanici_saat_dilimi = tracker.get_slot("timezone") or "Europe/Istanbul"
                zaman_bilgisi = datetime.now(pytz.timezone(kullanici_saat_dilimi))
                turkce_zaman = turkce_tarih_zamani_formatla(zaman_bilgisi)

                mesaj = f"Bugün {turkce_zaman}."
                dispatcher.utter_message(text=mesaj)
        except Exception as e:
            dispatcher.utter_message(text="Üzgünüm, zaman bilgisi alınırken bir hata oluştu.")

        return []

    def get_timezone_for_city(self, city: str) -> str:
        city_timezone_map = {
            # Avrupa
            "londra": "Europe/London",
            "paris": "Europe/Paris",
            "berlin": "Europe/Berlin",
            "madrid": "Europe/Madrid",
            "roma": "Europe/Rome",
            "amsterdam": "Europe/Amsterdam",
            "moskova": "Europe/Moscow",
            "helsinki": "Europe/Helsinki",
            "istanbul": "Europe/Istanbul",
            "athens": "Europe/Athens",

            # Amerika
            "new york": "America/New_York",
            "los angeles": "America/Los_Angeles",
            "chicago": "America/Chicago",
            "toronto": "America/Toronto",
            "mexico city": "America/Mexico_City",
            "sao paulo": "America/Sao_Paulo",
            "buenos aires": "America/Argentina/Buenos_Aires",
            "vancouver": "America/Vancouver",
            "miami": "America/New_York",

            # Asya
            "tokyo": "Asia/Tokyo",
            "seul": "Asia/Seoul",
            "pekin": "Asia/Shanghai",
            "bangkok": "Asia/Bangkok",
            "kuala lumpur": "Asia/Kuala_Lumpur",
            "hanoi": "Asia/Ho_Chi_Minh",
            "manila": "Asia/Manila",
            "tahran": "Asia/Tehran",
            "dubai": "Asia/Dubai",
            "delhi": "Asia/Kolkata",
            "hong kong": "Asia/Hong_Kong",

            # Afrika
            "kahire": "Africa/Cairo",
            "lagos": "Africa/Lagos",
            "cape town": "Africa/Johannesburg",
            "nairobi": "Africa/Nairobi",
            "casablanca": "Africa/Casablanca",
            "addis ababa": "Africa/Addis_Ababa",

            # Okyanusya
            "sydney": "Australia/Sydney",
            "melbourne": "Australia/Melbourne",
            "brisbane": "Australia/Brisbane",
            "auckland": "Pacific/Auckland",
            "fiji": "Pacific/Fiji",
            "honolulu": "Pacific/Honolulu",

            # Orta Doğu
            "riyad": "Asia/Riyadh",
            "bağdat": "Asia/Baghdad",
            "tel aviv": "Asia/Jerusalem",
            "kuveyt": "Asia/Kuwait",
            "beyrut": "Asia/Beirut",
        }

        city = city.lower()
        return city_timezone_map.get(city)
