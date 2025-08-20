import os
import shutil
import subprocess
from datetime import datetime

# Projekt navn
APP_NAME = "Fundora"
MAIN_SCRIPT = "Ctk_fundora_app.py"

# Mapper
DIST_DIR = "dist"
ONEDIR_DIR = os.path.join(DIST_DIR, "onedir")
ONEFILE_DIR = os.path.join(DIST_DIR, "onefile")


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")

    # ONEDIR version
    version_onedir = get_next_version(os.path.join(ONEDIR_DIR, "versions"), APP_NAME)
    build_onedir(version_onedir, date_str)

    # ONEFILE version
    version_onefile = get_next_version(os.path.join(ONEFILE_DIR, "versions"), APP_NAME)
    build_onefile(version_onefile, date_str)

    print("\n✅ Build færdig!")
    print(f"  ONEDIR version: v{version_onedir:02d}")
    print(f"  ONEFILE version: v{version_onefile:02d}")


def get_next_version(versions_dir, prefix):
    """Find næste versionsnummer baseret på eksisterende builds"""
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
        return 1

    existing = [d for d in os.listdir(versions_dir) if d.startswith(prefix)]
    if not existing:
        return 1

    nums = []
    for d in existing:
        try:
            num = int(d.split("_")[1][1:])  # henter tallet efter vXX
            nums.append(num)
        except:
            pass
    return max(nums) + 1 if nums else 1

def build_onedir(version, date_str, mode="release"):
    """Byg ONEDIR version"""
    print("Bygger ONEDIR...")
    versions_dir = os.path.join(ONEDIR_DIR, "versions")
    published_dir = os.path.join(ONEDIR_DIR, "_published")

    build_name = f"{APP_NAME}_v{version:02d}_{date_str}"
    build_path = os.path.join(versions_dir, build_name)

    console_flag = "--console" if mode == "debug" else "--noconsole"


    # Kør pyinstaller
    subprocess.run([
        "pyinstaller", "--onedir",console_flag, MAIN_SCRIPT,
        "--add-data", "Images;Images",
        "--add-data", "backend;backend",
        "--add-data", "components;components",
        "--add-data", "database;database",
        "--add-data", "gui;gui",
        "--hidden-import", "fpdf",
        "--hidden-import", "mysql",
        "--hidden-import", "mysql.connector",
        "--hidden-import", "sqlite3",
        "--collect-binaries", "sqlite3",
        "--hidden-import", "bcrypt",
        "--hidden-import", "_cffi_backend",
        "--noconfirm",
        "--distpath", versions_dir,
        "--name", build_name
    ], check=True)

    # Published = clean navn uden version/dato
    if os.path.exists(published_dir):
        shutil.rmtree(published_dir)
    shutil.copytree(build_path, os.path.join(published_dir, APP_NAME))

def build_onefile(version, date_str, mode="release"):
    """Byg ONEFILE version"""
    print("Bygger ONEFILE...")
    versions_dir = os.path.join(ONEFILE_DIR, "versions")
    published_dir = os.path.join(ONEFILE_DIR, "_published")

    os.makedirs(versions_dir, exist_ok=True)
    os.makedirs(published_dir, exist_ok=True)

    build_name = f"{APP_NAME}_v{version:02d}_{date_str}.exe"
    build_path = os.path.join(versions_dir, build_name)
    published_path = os.path.join(published_dir, f"{APP_NAME}.exe")

    console_flag = "--console" if mode == "debug" else "--noconsole"

    # Kør pyinstaller
    subprocess.run([
        "pyinstaller", "--onefile", console_flag, MAIN_SCRIPT,
        "--add-data", "Images;Images",
        "--add-data", "backend;backend",
        "--add-data", "components;components",
        "--add-data", "database;database",
        "--add-data", "gui;gui",
        "--hidden-import", "fpdf",
        "--hidden-import", "mysql",
        "--hidden-import", "mysql.connector",
        "--hidden-import", "sqlite3",
        "--collect-binaries", "sqlite3",
        "--hidden-import", "bcrypt",
        "--hidden-import", "_cffi_backend",
        "--noconfirm",
        "--distpath", versions_dir,
        "--name", build_name.replace(".exe", "")
    ], check=True)

    # Kopi til published (clean navn)
    if os.path.exists(published_path):
        os.remove(published_path)
    shutil.copy2(build_path, published_path)


if __name__ == "__main__":
    main()

