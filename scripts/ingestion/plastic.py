"""
================================================================
  Scraper Harga Plastik — FIXED: Selalu ambil data terbaru
================================================================
  3 perbaikan utama:
  1. Klik tombol MAX di browser sebelum ambil data
  2. Gunakan parameter tanggal eksplisit di URL
  3. Validasi & log tanggal terakhir data
================================================================
"""

import os, time, json, re, requests, pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

os.environ['TEDATA_DISABLE_LOGGING'] = 'true'


# ================================================================
# [FIX 2] URL dengan parameter tanggal eksplisit
# ================================================================
def get_tanggal_range(tahun_ke_belakang: int = 5):
    hari_ini    = datetime.now().strftime("%Y-%m-%d")
    tanggal_awal = (datetime.now() - timedelta(days=tahun_ke_belakang * 365)).strftime("%Y-%m-%d")
    return tanggal_awal, hari_ini


# ================================================================
# [FIX 3] Validasi kelengkapan data
# ================================================================
def cek_kelengkapan_data(df: pd.DataFrame):
    if df is None or df.empty:
        print("[CEK] ⚠ DataFrame kosong!")
        return

    df["tanggal"] = pd.to_datetime(df["tanggal"])
    tanggal_terakhir = df["tanggal"].max()
    hari_ini         = pd.Timestamp.now().normalize()
    selisih          = (hari_ini - tanggal_terakhir).days

    print(f"\n{'─'*55}")
    print(f"[CEK] Tanggal awal data  : {df['tanggal'].min().date()}")
    print(f"[CEK] Tanggal akhir data : {tanggal_terakhir.date()}")
    print(f"[CEK] Hari ini           : {hari_ini.date()}")
    print(f"[CEK] Selisih            : {selisih} hari")
    print(f"[CEK] Total baris        : {len(df)}")

    if selisih == 0:
        print("[CEK] ✓✓ Data sudah sampai hari ini!")
    elif selisih <= 3:
        print(f"[CEK] ✓ Data relatif terkini (lag {selisih} hari — normal untuk komoditas)")
    elif selisih <= 7:
        print(f"[CEK] ⚠ Data lag {selisih} hari — cek apakah sumber belum update")
    else:
        print(f"[CEK] ✗ Data sudah {selisih} hari tidak update! Perlu investigasi.")
    print(f"{'─'*55}\n")


# ================================================================
# SETUP DRIVER
# ================================================================
def setup_firefox_driver(headless: bool = True):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager

    opts = Options()
    if headless:
        opts.add_argument("--headless")
    opts.set_preference("general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0")
    opts.set_preference("dom.webnotifications.enabled", False)
    opts.set_preference("app.update.enabled", False)

    print("[Driver] Setup geckodriver …")
    service = Service(GeckoDriverManager().install())
    driver  = webdriver.Firefox(service=service, options=opts)
    print("[Driver] ✓ Firefox siap!")
    return driver


# ================================================================
# METODE 1 — tedata
# ================================================================
def coba_tedata_fixed() -> pd.DataFrame | None:
    try:
        import tedata as ted
    except ImportError:
        print("[tedata] Belum install: pip install tedata")
        return None

    try:
        from webdriver_manager.firefox import GeckoDriverManager
        driver_path = GeckoDriverManager().install()
        os.environ["PATH"] = os.path.dirname(driver_path) + os.pathsep + os.environ["PATH"]
    except Exception as e:
        print(f"[tedata] Gagal set geckodriver: {e}")

    url = "https://tradingeconomics.com/commodity/polyethylene"
    print(f"[tedata] Scraping: {url}")

    try:
        hasil = ted.scrape_chart(url=url, method="highcharts_api", headless=True)
        if hasil is not None and hasattr(hasil, 'data') and hasil.data is not None:
            df = hasil.data.reset_index()
            df.columns = ["tanggal", "harga"]
            df["satuan"] = "CNY/T"
            df["sumber"] = "tedata"
            print(f"[tedata] ✓ {len(df)} baris!")
            return df
    except Exception as e:
        print(f"[tedata] Error: {e}")
    return None


# ================================================================
# METODE 2 — Selenium + [FIX 1] klik MAX + [FIX 2] tanggal URL
# ================================================================
def coba_selenium_highcharts() -> pd.DataFrame | None:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    print("\n[Selenium] Membuka halaman …")

    try:
        driver = setup_firefox_driver(headless=True)
    except Exception as e:
        print(f"[Selenium] Gagal buat driver: {e}")
        return None

    url = "https://tradingeconomics.com/commodity/polyethylene"

    try:
        driver.get(url)
        print("[Selenium] Halaman dimuat, tunggu render JS …")
        time.sleep(6)

        # ── [FIX 1] Klik tombol MAX / All untuk load semua data ─
        print("[Selenium] Mencari tombol MAX …")
        max_diklik = False
        try:
            # Coba berbagai selector tombol range
            selectors = [
                "//button[normalize-space()='MAX']",
                "//button[normalize-space()='max']",
                "//a[normalize-space()='MAX']",
                "//span[normalize-space()='MAX']",
                "//li[normalize-space()='MAX']",
                "//*[@data-type='MAX']",
            ]
            for sel in selectors:
                tombol = driver.find_elements(By.XPATH, sel)
                if tombol:
                    tombol[0].click()
                    print(f"[Selenium] ✓ Klik MAX via XPATH: {sel}")
                    max_diklik = True
                    time.sleep(3)
                    break

            # Fallback: klik via JavaScript
            if not max_diklik:
                result = driver.execute_script("""
                    var btns = document.querySelectorAll('button, a, span, li');
                    for (var b of btns) {
                        if (b.textContent.trim() === 'MAX' || b.textContent.trim() === 'max') {
                            b.click();
                            return 'klik:' + b.tagName;
                        }
                    }
                    return null;
                """)
                if result:
                    print(f"[Selenium] ✓ Klik MAX via JS: {result}")
                    max_diklik = True
                    time.sleep(3)

            if not max_diklik:
                print("[Selenium] ⚠ Tombol MAX tidak ditemukan, lanjut tanpa klik")

        except Exception as e:
            print(f"[Selenium] Gagal klik MAX: {e}")

        # ── Ambil data Highcharts ──────────────────────────────
        js_highcharts = """
        try {
            var charts = Highcharts.charts.filter(c => c !== undefined);
            if (charts.length === 0) return null;
            var chart = charts[0];
            var series = chart.series[0];
            if (!series) return null;
            return JSON.stringify({
                data: series.options.data || [],
                xData: series.processedXData || [],
                yData: series.processedYData || [],
                name: series.name,
                unit: chart.yAxis[0].axisTitle ? chart.yAxis[0].axisTitle.textStr : ''
            });
        } catch(e) { return 'ERR:' + e.message; }
        """
        result = driver.execute_script(js_highcharts)
        print(f"[Selenium] Highcharts result: {str(result)[:200]}")

        if result and not str(result).startswith("ERR"):
            try:
                obj   = json.loads(result)
                data  = obj.get("data", [])
                xData = obj.get("xData", [])
                yData = obj.get("yData", [])
                records = []

                if data and isinstance(data[0], (list, tuple)):
                    for pt in data:
                        records.append({
                            "tanggal": datetime.fromtimestamp(pt[0] / 1000).strftime("%Y-%m-%d"),
                            "harga":   pt[1],
                        })
                elif xData and yData:
                    for ts_ms, val in zip(xData, yData):
                        records.append({
                            "tanggal": datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d"),
                            "harga":   val,
                        })

                if records:
                    df = pd.DataFrame(records)
                    df["satuan"] = "CNY/T"
                    df["sumber"] = f"Trading Economics - {obj.get('name', 'Polyethylene')}"
                    print(f"[Selenium] ✓ Highcharts: {len(df)} titik data!")
                    driver.quit()
                    return df

            except Exception as e:
                print(f"[Selenium] Parse Highcharts gagal: {e}")

        # ── [FIX 2] Coba endpoint dengan tanggal eksplisit ─────
        print("[Selenium] Coba endpoint dengan tanggal eksplisit …")
        d_awal, d_akhir = get_tanggal_range(tahun_ke_belakang=10)
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}
        driver.quit()

        endpoint_candidates = [
            f"https://markets.tradingeconomics.com/chart?s=polyethylene&d1={d_awal}&d2={d_akhir}&type=line",
            f"https://api.tradingeconomics.com/charts/historical/polyethylene?d1={d_awal}&d2={d_akhir}",
            f"https://tradingeconomics.com/charts/chart.aspx?s=polyethylene&d1={d_awal}&d2={d_akhir}",
        ]

        headers = {
            "User-Agent":  "Mozilla/5.0 Firefox/125.0",
            "Referer":     "https://tradingeconomics.com/",
            "Accept":      "application/json",
        }

        for url_api in endpoint_candidates:
            try:
                print(f"[Selenium] Coba: {url_api[:80]}…")
                resp = requests.get(url_api, cookies=cookies, headers=headers, timeout=15)
                print(f"[Selenium] Status: {resp.status_code}")
                if resp.status_code == 200:
                    d = resp.json()
                    if isinstance(d, list) and len(d) > 5:
                        records = []
                        for pt in d:
                            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                                records.append({
                                    "tanggal": datetime.fromtimestamp(pt[0] / 1000).strftime("%Y-%m-%d"),
                                    "harga":   pt[1],
                                    "satuan":  "CNY/T",
                                    "sumber":  "Trading Economics API",
                                })
                        if records:
                            print(f"[Selenium] ✓ API: {len(records)} titik!")
                            return pd.DataFrame(records)
            except Exception as e:
                print(f"[Selenium] Endpoint gagal: {e}")

    except Exception as e:
        print(f"[Selenium] Error umum: {e}")
        try:
            driver.quit()
        except Exception:
            pass

    return None


# ================================================================
# METODE 3 — Intercept network
# ================================================================
def coba_intercept_network() -> pd.DataFrame | None:
    print("\n[Network] Intercept request jaringan …")

    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager

        opts = Options()
        opts.add_argument("--headless")
        service = Service(GeckoDriverManager().install())
        driver  = webdriver.Firefox(service=service, options=opts)

        driver.get("about:blank")
        driver.execute_script("""
        window._intercepted = [];
        var origFetch = window.fetch;
        window.fetch = function() {
            var url = arguments[0];
            if (typeof url === 'string' && (url.includes('chart') || url.includes('Chart'))) {
                origFetch.apply(this, arguments).then(function(resp) {
                    resp.clone().json().then(function(data) {
                        window._intercepted.push({url: url, data: data});
                    }).catch(function(){});
                });
            }
            return origFetch.apply(this, arguments);
        };
        """)

        driver.get("https://tradingeconomics.com/commodity/polyethylene")
        time.sleep(8)

        intercepted = driver.execute_script("return JSON.stringify(window._intercepted || []);")
        driver.quit()

        if intercepted:
            items = json.loads(intercepted)
            print(f"[Network] {len(items)} request terdeteksi")
            for item in items:
                data = item.get("data")
                if isinstance(data, list) and len(data) > 5:
                    records = []
                    for pt in data:
                        if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                            records.append({
                                "tanggal": datetime.fromtimestamp(pt[0]/1000).strftime("%Y-%m-%d"),
                                "harga":   pt[1],
                                "satuan":  "CNY/T",
                                "sumber":  "Trading Economics Network",
                            })
                    if records:
                        print(f"[Network] ✓ {len(records)} titik data!")
                        return pd.DataFrame(records)

    except Exception as e:
        print(f"[Network] Error: {e}")
    return None


# ================================================================
# SIMPAN
# ================================================================
def simpan(df: pd.DataFrame, label: str = "polyethylene"):
    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
    f_csv  = f"{ts}_harga_{label}.csv"
    f_xlsx = f"{ts}_harga_{label}.xlsx"
    f_json = f"{ts}_harga_{label}.json"

    df.to_csv(f_csv, index=False, encoding="utf-8-sig")
    df.to_json(f_json, orient="records", indent=2, force_ascii=False)
    try:
        df.to_excel(f_xlsx, index=False)
        print(f"  XLSX : {f_xlsx}")
    except Exception:
        pass

    print(f"\n  ✓ Data disimpan!")
    print(f"  CSV  : {f_csv}")
    print(f"  JSON : {f_json}")
    print(f"\nPreview (10 terakhir):")
    print(df.tail(10).to_string(index=False))


# ================================================================
# MAIN
# ================================================================
def main():
    print("=" * 60)
    print("  Scraper Harga Plastik — Fixed (selalu ambil terbaru)")
    print(f"  Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    df = None

    df = coba_tedata_fixed()
    if df is None:
        df = coba_selenium_highcharts()
    if df is None:
        df = coba_intercept_network()

    if df is None or len(df) <= 1:
        print("\n[INFO] Semua metode gagal. Mungkin TE memblokir.")
        df = pd.DataFrame([{
            "tanggal": datetime.now().strftime("%Y-%m-%d"),
            "harga":   None,
            "satuan":  "CNY/T",
            "sumber":  "Gagal scraping",
        }])

    # [FIX 3] Selalu cek kelengkapan sebelum simpan
    cek_kelengkapan_data(df)
    simpan(df)


if __name__ == "__main__":
    main()