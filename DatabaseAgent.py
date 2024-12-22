from jinja2 import Environment, BaseLoader

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData, Table, text

from ai360_inference2 import inference

import re

class DBAgent:
    def __init__(self, db_uri: str, prompt_file_path: str = None):
        self.engine = create_engine(db_uri)

        metadata = MetaData()
        metadata.reflect(self.engine)
        self.schema = DBAgent._schema_to_string(metadata.tables)

        if prompt_file_path is None: 
            import os
            path = os.getcwd()
            prompt_file = 'Agents\db.jinja2'
            prompt_file_path = os.path.join(path, prompt_file)

        with open(prompt_file_path) as f:
            self._prompt_template = f.read()

    @staticmethod
    def _schema_to_string(schema):
        schema_str = ""
        for table_name, table in schema.items():
            schema_str += f"- Table: {table_name}\n"
            for column in table.columns:
                schema_str += f"  - {column.name} ({column.type}"
                if column.primary_key:
                    schema_str += ", primary key"
                if column.foreign_keys:
                    fk = list(column.foreign_keys)[0].column
                    schema_str += f", foreign key referencing {fk.table.name}.{fk.name}"
                schema_str += ")\n"
        return schema_str

    def render(self, user_query: str) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(self._prompt_template)
        return template.render(user_query=user_query, database_schema=self.schema)

    def _invoke_llm(self, user_query: str, direct: bool = False) -> str:
        prompt = self.render(user_query=user_query) if not direct else user_query
        messages = [
            {
                "role": "user",
                "content": prompt.strip(),
            }
        ]
        response = inference(messages)

        return response


    @staticmethod
    def _extract_sql(response: str):
        match = re.search('@@(.*)@@', response, re.DOTALL)
        if match:
            sql_query = match.group(1)
            return sql_query
        else:
            return None

    def _get_results_from_response(self, response: str):
        sql = DBAgent._extract_sql(response=response)
        print(f"[EXTRACTED SQL]:\n{sql}")

        if sql is None:
            return None

        with self.engine.connect() as connection:
            result = connection.execute(text(sql))
            return result.fetchall()

    def execute(self, user_query: str):
        llm_response = self._invoke_llm(user_query=user_query)


        db_results = self._get_results_from_response(response=llm_response)
        print(f"[DB RESULTS]:\n{db_results}")

        prompt = f'''
        The user asked: {user_query}
        The relavent information is: {db_results}
        
        Structure the information into a proper response and give only the response.
'''.strip()

        return self._invoke_llm(user_query=prompt, direct=True)

