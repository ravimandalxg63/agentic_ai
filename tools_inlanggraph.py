from langgraph.graph import StateGraph,END,START
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import  requests
from tavily import TavilyClient

import os
os.environ["TAVILY_API_KEY"] = "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"
tavily_client=TavilyClient(api_key=os.getenv('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'))



# set llm
llm=ChatOllama(model='qwen2.5:3b')

serch_tool=DuckDuckGoSearchRun(region='us-en')
@tool
def  calculator(first_num:float,second_num:float,opration:str)->dict:
    """preform a basic arthematic opration on two number.
       supporyed opration: add,sub,mul,div"""
    try:
        if opration=='add':
            result=first_num+second_num
        elif opration=='sub':
            result=first_num+second_num
        elif opration=='div':
            if second_num==0:
                return {'error: f"unspooreded opration"'}
            result=first_num/second_num
        else:
            return {'error: f"unsported opration {opration}"'}
        return {'fist_num':first_num,'second_num':second_num,'opration':opration,'result':result}
    except Exception as e:
        return {'error':str(e)}

 
@tool
def serch_web(query:str)->str:
    """serch web for current information and news"""
    result=tavily_client.search(query=query,max_results=30,search_depth='advanced')
    return str(result)

#web_serch=tavily_client.search(query,max_results=29)
tools=[serch_tool,serch_web,calculator]

llm_with_tool=llm.bind_tools(tools=tools)
tole_node=ToolNode(tools=tools)
#from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import BaseMessage,add_messages
class chatstate(TypedDict):
    message:Annotated[list[BaseMessage],add_messages]

def chat_node(state:chatstate):
    messages=state['message']
    response=llm_with_tool.invoke(messages)
    return {'messages':[response]}

#chepoin=sqlite3.connect(database='chatbot.db',check_same_thread=False)
#conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
#checkpointer = SqliteSaver(conn=conn)


graph=StateGraph(chatstate)

graph.add_node('chat_node',chat_node)
graph.add_node('tools',tole_node)
graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)

chatbot=graph.compile()
inaal=chatbot.invoke({'messages':[HumanMessage(content='latest AI news')]})
print(inaal)


