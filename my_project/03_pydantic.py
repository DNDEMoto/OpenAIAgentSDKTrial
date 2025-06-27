from loguru import logger

from agents import Agent, Runner
from agents.tool import function_tool
from pydantic import BaseModel

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
        "札幌": {"temp": 15, "condition": "雹"},
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


# 構造化出力モデルの定義
logger.info("構造化出力モデルを定義しています...")

class WeatherResponse(BaseModel):
    location: str           # 場所
    temperature: float      # 気温
    unit: str               # 温度単位
    condition: str          # 天気状態
    recommendation: str     # おすすめ情報

logger.success("構造化出力モデルの定義が完了しました")

# 構造化出力を行うエージェントの作成
logger.info("構造化出力エージェントを作成しています...")

structured_agent = Agent(
    name="StructuredWeatherAgent",
    instructions="""
    あなたは構造化された天気情報を提供するアシスタントです。
    get_weather ツールを使用してデータを取得し、WeatherResponse形式で回答してください。
    """,
    tools=[get_weather],
    output_type=WeatherResponse
)

logger.success("構造化出力エージェントの作成が完了しました")

# 構造化出力エージェントのテスト
logger.info("構造化出力エージェントをテストします...")

# result = Runner.run_sync(structured_agent, "大阪の天気はどうですか？華氏で教えてください。")
result = Runner.run_sync(structured_agent, "札幌の天気はどうですか？")

logger.info(f"場所: {result.final_output.location}")
logger.info(f"気温: {result.final_output.temperature}°{result.final_output.unit}")
logger.info(f"天気: {result.final_output.condition}")
logger.info(f"おすすめ: {result.final_output.recommendation}")

logger.success("構造化出力エージェントのテストが完了しました")