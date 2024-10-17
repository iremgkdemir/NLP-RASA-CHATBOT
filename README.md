# Türkçe Chatbot Projesi
Bu proje, Rasa ve Flask kullanılarak oluşturulmuş bir Türkçe chatbot uygulamasıdır. Chatbot, kullanıcıdan alınan mesajlara göre hava durumu ve saat bilgisi gibi yanıtlar verebilmektedir.

**Not:** cd chatbot yazarak işlemler yapılır

## Gereksinimler
- **Python 3.7** veya daha yeni bir sürüm
- **Rasa Framework**
- **Flask**
- Diğer gerekli Python paketleri: `rasa-sdk`, `requests`, `pytz`, `flask`


## Kurulum
- **Gereksinimleri Yükleme**: 
- `pip install -r requirements.txt`
- `pip install flask`

- **Chatbot Eğitimi**:
-`rasa train`

- **Rasa Suncusunu Başlatma**:
- `rasa run --enable-api --cors "*"`
- `rasa run actions --port 5055`

- **Uygulamayı Başlat**:
- `python app.py `

- **Tarayıcıdan Adrese Git**
- `http://127.0.0.1:3000`
- Adreste açılan mavi baloncuğa tıklayarak sohbete başlayabilirsin


## Dosya Açıklamaları

- **`app.py`**: Flask ile yazılmış, sunucunun çalışmasını sağlayan ana dosya. Kullanıcıdan gelen mesajları alır ve Rasa'ya iletir.

- **`actions.py`**: Rasa'nın özel aksiyonlarını tanımlayan Python dosyası. Örneğin, hava durumu ve saat bilgisi almak için API çağrılarını içerir.

- **`config.yml`**: Rasa'nın yapılandırma ayarlarını içerir. Burada NLU (Doğal Dil Anlama) bileşenleri ve diyaloğun nasıl yönetileceği tanımlanır.

- **`credentials.yml`**: Botun Slack, Facebook Messenger gibi harici platformlarla entegrasyonu için gerekli kimlik bilgilerini içerir.

- **`domain.yml`**: Botun temel yapı taşlarını tanımlar. Bu dosyada niyetler (intents), varlıklar (entities), slotlar, yanıtlar ve aksiyonlar belirtilir.

- **`endpoints.yml`**: Rasa action sunucusu ve diğer harici bağlantıların yapılandırmasını içerir.

- **`index.html`**: Chatbot'un ön yüzünü sağlayan HTML dosyasıdır. Bootstrap ve jQuery kullanılarak basit bir sohbet arayüzü oluşturulmuştur.

- **`nlu.yml`**: Botun kullanıcı mesajlarını anlaması için gerekli eğitim verilerini içerir. Bu dosyada çeşitli niyetler için örnek kullanıcı ifadeleri tanımlanır.

- **`rules.yml`**: Botun belirli durumlarda nasıl davranacağını belirten kuralları tanımlar. Kural tabanlı diyaloğun nasıl yönetileceğini içerir.

- **`stories.yml`**: Botun olası kullanıcı etkileşimlerine nasıl yanıt vermesi gerektiğini belirleyen diyalog senaryolarını tanımlar. Örneğin, bir kullanıcının hava durumu sorduğu bir senaryo.