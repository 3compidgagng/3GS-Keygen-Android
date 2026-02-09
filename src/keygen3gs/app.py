name: Build BeeWare APK
on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
          
      - name: Install BeeWare Briefcase
        run: |
          pip install briefcase
          
      - name: Build Android APK
        run: |
          # Briefcase akan otomatis download Java & Android SDK
          briefcase build android
          briefcase package android
          
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: keygen-beeware
          path: dist/*.aab  # BeeWare biasanya output .aab (App Bundle) atau .apk
