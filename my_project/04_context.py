# コンテキストラッパーのインポート
from loguru import logger

from agents import Agent, Runner
from agents.tool import function_tool
from pydantic import BaseModel
from agents.run_context import RunContextWrapper

# カスタムコンテキストクラスの定義
logger.info("カスタムコンテキストクラスを定義しています...")

class ConversationContext:
    def __init__(self):
        # ユーザー設定を保存する辞書
        self.user_preferences = {}
        # 会話履歴を記録するリスト
        self.conversation_history = []
    
    def add_preference(self, key, value):
        """ユーザー設定を追加するメソッド"""
        self.user_preferences[key] = value
    
    def log_interaction(self, message):
        """会話を記録するメソッド"""
        self.conversation_history.append(message)

logger.success("カスタムコンテキストクラスの定義が完了しました")

# コンテキストを使用・更新するツールの作成
logger.info("コンテキスト操作ツールを作成しています...")

@function_tool
def set_preference(context: RunContextWrapper[ConversationContext], preference_key: str, preference_value: str) -> str:
    """
    会話コンテキストにユーザー設定を保存します。
    
    引数:
        preference_key: 設定の名前（例: 'temperature_unit'）
        preference_value: 設定の値（例: 'F'）
    
    戻り値:
        確認メッセージ
    """
    # コンテキストにユーザー設定を保存
    context.agent_context.add_preference(preference_key, preference_value)
    # 会話履歴に記録
    context.agent_context.log_interaction(f"{preference_key}の設定を{preference_value}に変更しました")
    return f"{preference_key}の設定を{preference_value}に変更しました。"

@function_tool
def get_user_preferences(context: RunContextWrapper[ConversationContext]) -> str:
    """
    保存されているユーザー設定をすべて取得します。
    
    戻り値:
        すべての設定を一覧表示した文字列
    """
    # コンテキストからユーザー設定を取得
    prefs = context.agent_context.user_preferences
    if not prefs:
        return "まだ設定がありません。"
    
    return "現在の設定: " + ", ".join([f"{k}: {v}" for k, v in prefs.items()])

logger.success("コンテキスト操作ツールの作成が完了しました")

# コンテキストを使用するエージェントの作成
logger.info("コンテキスト対応エージェントを作成しています...")

context_agent = Agent[ConversationContext](
    name="ContextAwareAgent",
    instructions="""
    あなたはユーザーの設定を記憶するアシスタントです。
    set_preference ツールを使用して設定を保存し、
    get_user_preferences ツールを使用して設定を取得してください。
    """,
    tools=[set_preference, get_user_preferences],
)

logger.success("コンテキスト対応エージェントの作成が完了しました")

# コンテキストインスタンスの作成
logger.info("コンテキストインスタンスを作成しています...")

my_context = ConversationContext()


# 最初のやり取り: 設定を保存
logger.info("1回目の会話: 設定を保存します...")

result1 = Runner.run_sync(
    context_agent,
    "温度は華氏で表示してほしいです。",
    context=my_context
)
logger.info(f"エージェントの回答: {result1.final_output}")

# 2回目のやり取り: 設定を取得
logger.info("2回目の会話: 保存した設定を確認します...")

# messages = [
#     Message.user("温度は華氏で表示してほしいです。"),
#     Message.assistant(result1.final_output),
#     Message.user("今までに設定した内容を教えてください。")
# ]

result2 = Runner.run_sync(
    context_agent,
    "今までに設定した内容を教えてください。",
    context=my_context
)
logger.info(f"エージェントの回答: {result2.final_output}")

logger.success("コンテキスト管理のテストが完了しました")