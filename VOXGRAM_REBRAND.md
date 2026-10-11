# Voxgram Desktop — rebrand

Форк Telegram Desktop (ранее Opengram). Voxgram — отдельное приложение:
свои UUID, папка данных, имя exe и URL-схема, поэтому он ставится рядом
с Telegram Desktop и старым Opengram и не конфликтует с ними.

## Что изменено

### 1. Название и константы
- `Telegram/SourceFiles/core/version.h`:
  - `AppId` = `{F35DD0AE-9A76-4DC4-9F46-C25CD709E2B5}`
  - `AppName` = `Voxgram Desktop` (папка данных `%AppData%\Voxgram Desktop`)
  - `AppFile` = `Voxgram`
- Windows AppUserModelID: `Voxgram.VoxgramDesktop` (`.Store` для UWP).
- Инсталлятор `Telegram/build/setup.iss`: тот же UUID, `Voxgram.exe`.
- macOS bundle id: `fun.voxgram.Voxgram`.
- Интерфейсные строки (`lang.strings`) и строки в C++: `Opengram` → `Voxgram`.

### 2. Домен
Все ссылки `opengra.me` → `voxgram.fun`: публичные ссылки
(`voxgram.fun/username`, `voxgram.fun/+invite`), сайт, FAQ, адрес апдейтера.
Журнал изменений → https://github.com/voxgram-git/VoxgramDesktop/releases.

### 3. URL-схема
- В системе регистрируются `vg://` (основная) и `opengram://` (чтобы
  открывались ссылки от старых сборок).
- Внутри клиента `openLocalUrl()` принимает `vg://`, `opengram://` и `tg://`.
- `tg://` в системе не регистрируется — его по-прежнему открывает
  Telegram Desktop, если он установлен.
- Где прописано: `core/application.cpp`, `Telegram.plist`,
  `uwp/AppX/AppxManifest.xml`, `lib/xdg/org.telegram.desktop.desktop`.

### 4. Лого
- Исходник: `Telegram/Resources/art/voxgram_logo.svg`.
- Все растровые иконки генерирует `Telegram/Resources/art/voxgram_logo.py`
  (`pip install pillow cairosvg shapely`, затем `python3 Telegram/Resources/art/voxgram_logo.py`):
  `art/icon*.png`, `icon256.ico`, `logo_256*.png`, `icon_round512@2x.png`,
  иконки macOS (`Images.xcassets`), UWP (`uwp/AppX/Assets`) и лого на экране
  входа (`icons/intro_voxgram_logo*.png`), монохромные иконки трея
  (`icons/tray_monochrome*.svg`), иконку трея macOS и лого в QR-кодах.

### 5. Тема
Встроенные темы `day-blue` и `night` возвращены к оригинальным синим
цветам (в Opengram они были перекрашены в зелёный).

### 6. Ссылки voxgram.fun
- `https://voxgram.fun/...` открываются внутри клиента, как раньше `t.me`
  (`Core::TryConvertUrlToLocal`). Страницы сайта (`/#...`, `/legal`, `/faq`,
  `/donate`, `/privacy`, `/tos`, `/changelog`) открываются в браузере.
- Ссылки, которые строит клиент (юзернеймы, посты), всегда на
  `https://voxgram.fun/`, `me_url_prefix` из серверного конфига игнорируется.
- Ссылки от сервера (приглашения, ссылки на сообщения и истории, звонки)
  с `t.me` переписываются на `voxgram.fun` (`Core::VoxgramLinkFromServer`).
- Языковые пакеты с сервера: `Telegram`/`Телеграм` → `Voxgram`,
  `telegram.org`/`t.me` → `voxgram.fun` (`lang_instance.cpp`). FAQ всегда
  `https://voxgram.fun/#faq`, политика ботов и мини-приложений —
  `https://voxgram.fun/legal/bots`.

### 7. Адреса серверов
JSON-конфиг Opengram удалён. Адреса DC берутся только из `kBuiltInDcs`
в `mtproto/mtproto_dc_options.cpp` (сейчас `31.77.10.99:20443`), URL
апдейтера — `https://voxgram.fun`.

## RSA-ключ сервера

CI подставляет ключ из секрета репозитория `VOXGRAM_PUBKEY`
(Settings → Secrets and variables → Actions). Локально:

```
python _apply_pubkey.py   # читает pubkey.asc из корня репозитория
```
