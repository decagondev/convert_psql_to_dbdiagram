import os
from sqlalchemy import create_engine, MetaData
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo")

def read_postgresql_file(file_path):
    with open(file_path, 'r') as file:
        sql_content = file.read()
    return sql_content

prompt_template = PromptTemplate(
    input_variables=["sql_schema"],
    template="""
    You are an expert database designer.
    Convert the following PostgreSQL SQL schema into dbdiagram.io format:
    
    SQL Schema:
    {sql_schema}
    
    dbdiagram.io Code:
    """
)

def convert_sql_to_dbdiagram(sql_schema):
    chain = LLMChain(llm=llm, prompt=prompt_template)
    dbdiagram_code = chain.run(sql_schema)
    return dbdiagram_code

def write_to_file(output_file_path, content):
    with open(output_file_path, 'w') as file:
        file.write(content)
    print(f"dbdiagram.io code written to {output_file_path}")

def main(sql_file_path, output_file_path):
    sql_schema = read_postgresql_file(sql_file_path)
    
    dbdiagram_code = convert_sql_to_dbdiagram(sql_schema)
    
    write_to_file(output_file_path, dbdiagram_code)

if __name__ == "__main__":
    sql_file_path = "input.sql"
    output_file_path = "dbdiagram_code.txt"
    main(sql_file_path, output_file_path)

