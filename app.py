import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp, AsyncioExecutor
from schema import schema as rate_schema
from database.models import db_session

app = FastAPI()
app.add_route("/", GraphQLApp(schema=rate_schema, executor_class=AsyncioExecutor))

@app.on_event("shutdown")
def shutdown_session(exception=None):
    db_session.remove()
