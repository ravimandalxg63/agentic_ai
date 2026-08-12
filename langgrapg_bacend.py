from langgraph.graph import StateGraph,END,START
from pydantic import BaseModel
from typing import TypedDict,Annotated
from langgraph.graph.message import BaseMessage,add_messages
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver,InMemorySaver
#from dotenv import load_dotenv
#load_dotenv()

llm=ChatOllama(model='qwen2.5:3b')

class chatbotestate(TypedDict):
    message:Annotated[list[BaseMessage],add_messages]


# definr chat node
def chat_node(state:chatbotestate):
    message=state['message']
    response=llm.invoke(message)
    return{'message':[response]}

# chepointer
chepointer=InMemorySaver()

graph=StateGraph(chatbotestate)
graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)
chatbot=graph.compile(checkpointer=chepointer)
#chatbot

