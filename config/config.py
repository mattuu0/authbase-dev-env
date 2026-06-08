import secrets
import os
import sys

def generate_random_key(length=64):
    """
    暗号学的に安全なランダムキーを、指定された長さ（デフォルト64文字）で生成します。
    """
    return secrets.token_urlsafe(length)

def confirm_overwrite_all(files_to_check):
    """
    主要な設定ファイルが存在するかを確認し、上書きするかを尋ねます。
    上書きが許可されない場合はFalseを返します。
    """
    existing_files = [f for f in files_to_check if os.path.exists(f)]

    if existing_files:
        print("\n--- ファイルの上書き確認 ---")
        print(f"以下のファイルが既に存在します: {', '.join(existing_files)}")
        response = input("これらのファイルをすべて上書きしますか？ (y/n): ")
        if response.lower() != 'y':
            print("ファイルの生成を中止しました。")
            return False
    return True

def create_env_file(file_path, content):
    """
    指定されたファイルパスに、指定された内容で設定ファイルを生成します。
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content.strip())
    print(f"✅ ファイル '{file_path}' を生成しました。")

def main():
    """
    メイン処理：複数の設定ファイル生成関数を呼び出します。
    """
    # 作業ディレクトリを./dataに移動し、存在しなければ作成
    data_dir = "./data"
    os.makedirs(data_dir, exist_ok=True)
    os.chdir(data_dir)

    print("--- OAuth およびアプリケーション設定の開始 ---")

    # ファイルの上書き確認を行い、許可されない場合は終了
    files_to_check = ["auth.env", "app.env"]
    if not confirm_overwrite_all(files_to_check):
        return

    # app.env のテンプレート
    app_env_template = f"""
DB_TYPE = postgres
DB_DSN = host=db user=main password=main dbname=maindb port=5432 sslmode=disable TimeZone=Asia/Tokyo
"""

    # app.env ファイルを生成
    create_env_file("app.env", app_env_template)

    auth_env_template = f"""
DB_TYPE = postgres
DB_DSN = host=db user=main password=main dbname=maindb port=5432 sslmode=disable TimeZone=Asia/Tokyo

LOGIN_REDIRECT_URL = /ui/
APP_NAME = "SampleApp"
TOKEN_SECRET = "{generate_random_key()}"
ADMIN_SESSION_KEY = "{generate_random_key()}"
BRIDGE_TOKEN_SECRET = "{generate_random_key()}"
"""

    # auth.env ファイルを生成
    create_env_file("auth.env", auth_env_template)

    print(f"\n--- 設定完了！ ---")
    print(f"設定ファイルがすべて './data' ディレクトリに生成されました。")

if __name__ == "__main__":
    main()
