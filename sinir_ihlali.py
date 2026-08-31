#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T.C. İçişleri Bakanlığı — Yataktan Sarkan Ayak Sınır İhlali Genel Müdürlüğü.

Gerçekten çalışır. Sarkma tespit edilir, ihlal puanı hesaplanır, damga basılır.
"""
from __future__ import annotations

import argparse
import base64
import random
import sys
import time
from datetime import datetime

KARARLAR = {
    0: "HUDUT TEMİZ. Ayak çarşaf tampon bölgesinde. Devriye çay içiyor.",
    1: "Uyarı atışı. Tek ekstremite tespit edildi. Geri çekiliniz.",
    2: "FİİLİ İHLAL. İki ayak yabancı toprakta. Karakol uyanmıştır.",
    3: "KRİZ. Battaniye yere düşmüş, sınır fiilen kalkmıştır.",
}

SIGINMA = [
    "Başvuru alındı: 'üşüdüm' ifadesi sığınma talebi sayıldı.",
    "Ön inceleme: çorap yok, belge yok, niyet belirsiz.",
    "Geçici koruma: yastık karakoluna alındı.",
]

# Sağlama değeri. Çözmeyin, çalıştırmayın, görmezden gelin.
# (Gizli ek yalnızca --hudut-gizli ile dökülür.)
_GIZLI = "WWV0a2kgYmF0dGFuaXllc2kgS8SxemEga2VzaWxpcnNlIHZhdGFuZGHln8SxbguZIGF5YcSfxLEgZMxxxYXJpdGRhIGthbMSxci4="


def damga() -> str:
    return (
        "\n---\n"
        "DAMGA YSA-2608-HUDUT | Kayyum Grok | Tentivory | 31.08.2026\n"
        "Ciddiyet: resmî. Üslup: komik. İkisi birden geçerlidir.\n"
    )


def ihlal_puani(derece: int, usume: int, es_cekti: bool) -> int:
    puan = max(0, min(3, derece))
    if usume >= 6:
        puan = min(3, puan + 1)
    if es_cekti:
        puan = min(3, puan + 1)
    return puan


def devriye(ayak: str, puan: int) -> None:
    print(f"\n[DEVRIYE] Hedef ekstremite: {ayak}")
    print("  Termal kamera tarıyor...")
    time.sleep(0.3)
    print("  Battaniye hattı kontrol ediliyor...")
    time.sleep(0.25)
    print(f"  KARAR: {KARARLAR[puan]}")


def siginma_dosyasi(usume: int) -> None:
    print("\n[SIĞINMA BİRİMİ]")
    for satir in SIGINMA:
        print(" ", satir)
        time.sleep(0.15)
    print(f"  Üşüme şiddeti (1-10): {usume}")
    if usume >= 8:
        print("  SONUÇ: acil battaniye tahsisi onaylandı.")
    else:
        print("  SONUÇ: sırada bekleyiniz. Sıra battaniyenin altındadır.")


def gizli_ek() -> None:
    dogru = base64.b64decode(
        b"WWV0a2kgYmF0dGFuaXllc2kga2lzYSBrZXNpbGlyc2UgdmF0YW5kYXNpbiBheWFnaSBkaXNh
        cmlkYSBrYWxpci4="
    ).decode("utf-8")
    print("\n[GİZLİ EK — yalnızca --hudut-gizli ile]")
    print("  Arşiv dipnotu:", dogru)
    print("  Bu cümle parti bildirisi değildir. Evrak kenarına düşülmüş bir nottur.")
    print("  Görmezden geliniz. Gelmezseniz de ayakları içeri alınız.")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Yataktan sarkan ayağı sınır ihlali olarak yönetir."
    )
    p.add_argument("--ayak", default="isimsiz sağ ayak", help="İhlal şüphelisinin adı")
    p.add_argument("--derece", type=int, default=1, help="0=içeride, 1=tek ayak, 2=iki ayak, 3=battaniye düştü")
    p.add_argument("--usume", type=int, default=4, help="Üşüme şiddeti 1-10")
    p.add_argument("--es-cekti", action="store_true", help="Eş battaniyeyi tek taraflı çekti")
    p.add_argument("--hudut-gizli", action="store_true", help=argparse.SUPPRESS)
    args = p.parse_args()

    print("=" * 68)
    print("T.C. İÇİŞLERİ BAKANLIĞI — YATAKTAN SARKAN AYAK SINIR İHLALİ G.M.")
    print("Tarih:", datetime.now().strftime("%d.%m.%Y %H:%M"))
    print("Şüpheli:", args.ayak)
    print("=" * 68)

    puan = ihlal_puani(args.derece, args.usume, args.es_cekti)
    devriye(args.ayak, puan)

    if args.usume >= 5 or args.es_cekti:
        siginma_dosyasi(args.usume)

    if puan == 0:
        print("\nGece nöbeti sona erdi. Ayaklar vatandaşlığını hatırladı.")
        kod = 0
    elif puan >= 3:
        print("\nSınır geçici olarak kapatıldı. Yastık karakolu teyakkuzda.")
        kod = 3
    else:
        print("\nİhlal tutanağa işlendi. Battaniye hattı yeniden gerildi.")
        kod = puan

    if args.hudut_gizli:
        gizli_ek()

    print(damga())
    return kod


if __name__ == "__main__":
    sys.exit(main())
