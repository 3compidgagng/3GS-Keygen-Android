[app]

# (str) Title of your application
title = 3GS Keygen 21

# (str) Package name
package.name = keygen3gs

# (str) Package domain (needed for android/ios packaging)
package.domain = org.3gspatch

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# WAJIB: Kivy 2.3.0 & KivyMD 1.2.0 agar jalan di Python 3.12 Colab
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pycryptodome,pillow,openssl,libffi

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API
# KITA PAKAI 31 (Android 12) -> Paling Stabil dengan NDK r25b
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android NDK version to use
# WAJIB DIKUNCI DI r25b (Jangan dihapus baris ini)
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Permissions
android.permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE

# (list) The Android archs to build for.
# HANYA arm64-v8a agar build CEPAT
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True

# (str) The format used to package the app for debug mode
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android branch to use
# Kita balik ke master (stabil) karena develop sering berubah-ubah
p4a.branch = master

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2


[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1