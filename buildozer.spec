[app]

# (str) Título do aplicativo exibido no Android
title = Tarot Mistico

# (str) Nome do pacote interno (sem espaços ou caracteres especiais)
package.name = tarotmistico

# (str) Domínio reverso do pacote (identificador único na Play Store)
package.domain = org.vinicius

# (str) Diretório onde está o main.py
source.dir = .

# (list) Extensões de arquivo incluídas no pacote Android
source.include_exts = py,png,jpg,kv,atlas

# (list) Diretórios ignorados no empacotamento para reduzir o tamanho final
source.exclude_dirs = tests, bin, .venv, venv, __pycache__, .pytest_cache, .git

# (str) Versão do aplicativo
version = 1.0.1

# (list) Dependências Python e receitas compiladas pelo python-for-android
# Usa pacotes pure-Python para requests/urllib3 evitando binários x86_64 no ARM64
requirements = python3,kivy==2.3.1,requests==2.31.0,urllib3==1.26.18,chardet,idna,certifi,sqlite3,openssl

# (str) Ícone e tela de abertura (Splash Screen) do aplicativo
icon.filename = %(source.dir)s/assets/images/0_o_louco.png
presplash.filename = %(source.dir)s/assets/images/bg_tarot.png
presplash.color = #0F0D1F

# (list) Orientação da tela (portrait = vertical)
orientation = portrait

# (bool) 0 mantém a barra de status do Android visível; 1 ativa tela cheia
fullscreen = 0

#
# Configurações específicas do Android
#

# (list) Permissões necessárias (INTERNET obrigatória para o Firebase Auth)
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API (33 evita o crash de BroadcastReceiver do SDL2 2.26 no Android 14+)
android.api = 33

# (int) Mínimo Android API suportado (Android 7.0+)
android.minapi = 24

# (str) Versão do Android NDK recomendada pelo python-for-android
android.ndk = 25b

# (bool) Aceita automaticamente as licenças do Android SDK durante o build
android.accept_sdk_license = True

# (list) Arquiteturas alvo (arm64-v8a cobre dispositivos Android modernos e acelera o build)
android.archs = arm64-v8a

# (str) Versão estável do python-for-android compatível com Kivy 2.3.1 (Python 3.11)
p4a.branch = release-2024.01.21

# (bool) Permite backup automático de dados do app pelo Android
android.allow_backup = True

# (str) Formato do pacote no modo release (aab para Google Play Store, apk para instalação direta)
android.release_artifact = aab

# (str) Formato do pacote no modo debug (apk para testar direto no celular)
android.debug_artifact = apk


[buildozer]

# (int) Nível de log (2 = detalhado para acompanhar a compilação)
log_level = 2

# (int) Avisar caso executado como superusuário (root)
warn_on_root = 1
