from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner,InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio
from typing import Annotated, Literal

class HomeworkOutput(BaseModel):
    is_homework: bool
    homework_like_level_0_to_9 : int
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

class HomeworkAnswer(BaseModel):
    answer: str
    answer_number_if_exists: float
    question_level: Literal['element-school', 'high-school','university']  

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    output_type=HomeworkAnswer,
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    output_type=HomeworkAnswer,
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    print(result)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    try:
        #result = await Runner.run(triage_agent, "what is the value of pi?")
        
        #result = await Runner.run(triage_agent, "1+1=?")
        #print(result.final_output)

        result = await Runner.run(triage_agent, "who was the first president of the united states?")
        #result = await Runner.run(triage_agent, "日本で寺院の僧侶養成機関が始まったのは何時代ですか?")
        print(result.final_output)

        #result = await Runner.run(triage_agent, "what is life")
        #print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Tripwire triggered! The input was not flagged as homework.")

if __name__ == "__main__":
    asyncio.run(main())