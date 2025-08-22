import accountapi
from langchain_groq import ChatGroq
from langchain_core.language_models.llms import BaseLLM
from langchain_core.callbacks import CallbackManagerForLLMRun
from typing import Optional, List, Dict, Any
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool, StructuredTool
from dotenv import load_dotenv


load_dotenv()


llm = ChatGroq(model_name="llama3-70b-8192")


existence_checker = Tool(name = "existence_checker",
                         func = accountapi.user_exists,
                         description= "Use this tool if you want to know if a user exists, do not assume anything m wait till the tool gives you the output. This tool takes a single input : user_id")
authenticator = StructuredTool.from_function(name = "authenticator",
                     func = accountapi.authenticate_user,
                     description="Use this tool if you want to know if a user with a user id and password exists or not. Do not guess anything on your own. Wait until you get response from the tool .Use only this tool if you need to check the presence of a user. Do not forget that you have to use this tool only if you have both user id and password.This tool takes a two inputs : user_id , password. Do not use this tool if you do not have any of the inputs")
balancer_checker = Tool(name = "balancer_checker", 
                        func = accountapi.get_balance,
                        description="Use this tool if you want to know the balance of a user with some user id. Do not assume anything on your own. Use only this tool to check the balance of a user id. This tool takes a single input : user_id")
money_transferer = StructuredTool.from_function(name = "money_transferer",
                       func = accountapi.transfer_money,
                       description="Use this function if you want to transfer some money from an account to other account. Do not assume anything on you own. Use only this tool to transfer money. Do not assume that money has been transferred before you get the output from the tool .This tool takes 3 inputs : from_user , to_user , amount")
account_creator = Tool(name = "account_creator" ,
                       func = accountapi.create_account,
                       description="Use this tool if you want to create an account for a person. Do not assume anything on your own. Use only this tool for account creation. This tool takes a single input : user_name")
account_deletor = Tool(name = "account_deletor" ,
                       func = accountapi.delete_account,
                       description="Use this tool if you want to delete an account a user with some user_id. Do not assume anything on your own. Use only this tool for account deletion. Use this tool only if you have a user id. This tool takes a single input : user_id")
agent = initialize_agent(tools = [authenticator , balancer_checker , money_transferer , account_creator , account_deletor],
                         llm = llm,
                         agent = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                         verbose = True)
# if(__name__ == "main"):
# query = "Check my balance , user id is 20"
# respose = agent.invoke(query)
# print(respose["output"])