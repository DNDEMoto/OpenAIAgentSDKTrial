from loguru import logger

from agents import Agent, Runner
from agents.tool import function_tool
from pydantic import BaseModel


# 天気情報を取得するツールの定義
logger.info("天気情報ツールを作成しています...")

@function_tool
def get_weather(location: str, unit: str = "C") -> str:
    """
    指定された場所の天気情報を取得します。
    
    引数:
        location: 都市名や国名
        unit: 温度の単位、'C'（摂氏）または'F'（華氏）
    
    戻り値:
        現在の天気情報を含む文字列
    """
    # 実際の実装ではAPI呼び出しを行いますが、ここではモックデータを使用
    weather_data = {
        "東京": {"temp": 22, "condition": "晴れ"},
        "大阪": {"temp": 24, "condition": "曇り"},
        "札幌": {"temp": 15, "condition": "雨"},
        "福岡": {"temp": 26, "condition": "快晴"}
    }
    
    # 場所が見つからない場合のデフォルト値
    weather = weather_data.get(location, {"temp": 20, "condition": "不明"})
    
    # 必要に応じて温度変換
    temp = weather["temp"]
    if unit.upper() == "F":
        temp = (temp * 9/5) + 32

    return f"{location}の天気は{weather['condition']}で、気温は{temp}°{unit.upper()}です。"
    #return f"{location}:{weather['condition']}、気温:{temp}°{unit.upper()}"

logger.success("天気情報ツールの作成が完了しました")

# 天気ツールを使用するエージェントの作成
logger.info("天気アシスタントエージェントを作成しています...")

weather_agent = Agent(
    name="WeatherAssistant",
    instructions="""
    あなたは天気情報を提供するアシスタントです。
    天気に関する質問には get_weather ツールを使用してください。
    ユーザーが温度単位（C または F）を指定しているか確認してください。
    """,
    tools=[get_weather]
)

logger.success("天気アシスタントエージェントの作成が完了しました")

# 天気エージェントのテスト
logger.info("天気エージェントをテストします...")

result = Runner.run_sync(weather_agent, "東京の天気はどうですか？ケルビンに変換して教えて")
logger.info(f"エージェントの回答: {result.final_output}")

logger.success("天気エージェントのテストが完了しました")
