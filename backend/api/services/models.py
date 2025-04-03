from langchain_ollama import ChatOllama
from api.utils import params_check, cmd
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate, PromptTemplate


def ask(modelName, message):


    if not params_check.checkModel(modelName):
        raise "Error to find model"

    model = ChatOllama(model=modelName)

    response  = model.invoke(message)

    #print(response)

    return response



def agent(modelName, tools, message):


    if not params_check.checkModel(modelName):
        raise "Error to find model"

    model = ChatOllama(model=modelName)

    llmTools = []

    for tool in tools:
 
        llmTools.append(Tool(
        name=tool["NAME"],
        func=cmd.run_command,
        description=tool["DESCRIPTION"]
    ))


    
    llPrompt = PromptTemplate(
    input_variables=["agent_scratchpad",'input', 'tool_names', 'tools'],
    template='''
"""Answer the following questions as best as you can. You have access to the following tools:
{tools}.

Use the following format exactly as shown:

Thought: You should always think about what to do
Action: The action to take, should be one of {tool_names}
Action Input: The exact input to the action (do not modify it)

Observation: The result of the action

... (this Thought/Action/Action Input/Observation pattern may repeat N times)

**Rules:**
- Use the input exactly as received.
- Do **not** modify user input.

If the execution is successful:
Thought: I now know the final answer

Once the Final Answer is reached, stop and do not continue. There should be no additional actions after "Final Answer".

Begin!

Question: {input}
Thought: {agent_scratchpad}''')

    agent = create_react_agent(
            tools=llmTools,
            llm=model,
            prompt=llPrompt,
        )
        

    agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=llmTools,
    verbose=True,
    handle_parsing_errors=True,
    remember_intermediate_steps = True,
    return_intermediate_steps=True

    )
    
    
    response = agent_executor.invoke({'input': message})

    print(response)

    return response