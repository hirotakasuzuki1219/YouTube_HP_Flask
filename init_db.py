"""
データベース初期化スクリプト
既存のtravelsデータをデータベースに移行します
"""
from app import app, db, Travel
from datetime import datetime

# 既存の旅行データ（map.jsから抽出）
existing_travels = [
    {
        "name": "成田国際空港",
        "lat": 35.776366,
        "lon": 140.386249,
        "note": "ここから世界一周をスタート！まずはエジプトへ",
        "youtube": "https://www.youtube.com/embed/MsZmu32UglE"
    },
    {
        "name": "エジプト・ギザ周辺",
        "lat": 29.972883,
        "lon": 31.128796,
        "note": "ピラミッド周辺を観光ツアーに参加",
        "youtube": "https://www.youtube.com/embed/_1sYoq9pQWg"
    },
    {
        "name": "大エジプト博物館",
        "lat": 29.995239,
        "lon": 31.119273,
        "note": "プレオープン中のレアな時期に潜入",
        "youtube": "https://www.youtube.com/embed/-6LvRT89h_k"
    },
    {
        "name": "カイロ観光",
        "lat": 30.046261,
        "lon": 31.262404,
        "note": "アズハルモスクなどカイロ観光を堪能",
        "youtube": "https://www.youtube.com/embed/F1OhTilyzu0"
    },
    {
        "name": "カイロ脱出",
        "lat": 30.015892,
        "lon": 31.224700,
        "note": "閉じ込められて詰んだ",
        "youtube": "https://www.youtube.com/embed/k6KMBY0qDo8"
    },
    {
        "name": "カイロ国際空港",
        "lat": 30.12177042996925,
        "lon": 31.416275346081747,
        "note": "トルコへ移動！",
        "youtube": "https://www.youtube.com/embed/X7AN2xgwFTk"
    },
    {
        "name": "イスタンブール",
        "lat": 41.00539177063419,
        "lon": 28.96329556546734,
        "note": "イスタンブールでの日常を堪能",
        "youtube": "https://www.youtube.com/embed/_ubQxQfXTrw"
    },
    {
        "name": "アヤソフィアなど",
        "lat": 41.009284623958024,
        "lon": 28.980010132269836,
        "note": "イスタンブール観光！",
        "youtube": "https://www.youtube.com/embed/T-THt_l9TKQ"
    },
    {
        "name": "ザビハ・ギョクチェン国際空港",
        "lat": 40.89569332688844,
        "lon": 29.313471511623103,
        "note": "次の目的地はカッパドキアへ！",
        "youtube": "https://www.youtube.com/embed/fmsuShXs0Ds"
    },
    {
        "name": "カッパドキア",
        "lat": 38.63997623195001,
        "lon": 34.832035222971506,
        "note": "カッパドキアとは熱気球！",
        "youtube": "https://www.youtube.com/embed/M-5Dgpj45xo"
    },
    {
        "name": "ローズバレー",
        "lat": 38.659307136759445,
        "lon": 34.843411955828536,
        "note": "無料で大冒険！",
        "youtube": "https://www.youtube.com/embed/MiYJTreMAgY"
    },
]

def init_database():
    """データベースを初期化し、既存データを投入"""
    with app.app_context():
        # 既存のテーブルを削除して再作成
        db.drop_all()
        db.create_all()
        
        # 既存データを投入
        for travel_data in existing_travels:
            travel = Travel(
                name=travel_data['name'],
                lat=travel_data['lat'],
                lon=travel_data['lon'],
                note=travel_data.get('note', ''),
                youtube=travel_data.get('youtube', '')
            )
            db.session.add(travel)
        
        db.session.commit()
        print(f"{len(existing_travels)}件の旅行データをデータベースに追加しました。")

if __name__ == '__main__':
    init_database()

