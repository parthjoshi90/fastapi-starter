from functools import lru_cache
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    create_async_engine,
    async_sessionmaker,
)
from config.settings import get_settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from asyncpg.exceptions import InvalidCatalogNameError

settings = get_settings()

engin = create_async_engine(settings.DB_URI.unicode_string(), echo=True)

Base = declarative_base()


class DatabaseException(Exception):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message


class SQLiteException(Exception):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message


async def init_db():
    """
    Initialize the database by creating tables defined in the SQLAlchemy Base metadata.

    This function establishes a connection to the database engine, begins a transaction,
    and synchronously executes the creation of all tables defined in the SQLAlchemy Base
    metadata. The transaction is committed, and the connection is closed upon completion.

    Note:
    - Ensure that the `engine` is defined as a valid SQLAlchemy engine before calling this
      function.
    - This function is typically called during the application startup to ensure that
      database tables are created before handling requests.
    - For SQLite make sure to install the Async Driver to connect to the DB.

    Example:
    ```python
    engine = create_engine("postgresql+asyncpg://username:password@localhost:5432/your_database")
    await init_db()
    ```

    Raises:
    - Any exceptions raised during the database connection or table creation process
      will be propagated to the caller.
    """
    try:
        async with engin.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except InvalidRequestError as req_error:
        raise SQLiteException("InvalidRequestError", str(req_error._message))
    except InvalidCatalogNameError as db_error:
        raise DatabaseException("InvalidCatalogNameError", str(db_error))


@lru_cache
async def create_session():
    """
    Asynchronous function to create and return a scoped SQLAlchemy
    AsyncSession with a given engine.

    Returns:
        AsyncSession: A scoped asynchronous SQLAlchemy session.

    Note:
        This function utilizes the functools `lru_cache` decorator to
        cache and reuse the same session instance, avoiding unnecessary
        repeated creation during subsequent calls.
    """
    session = await async_scoped_session(
        async_sessionmaker(engin, expire_on_commit=False)
    )
    return session


async def get_session():
    """
    Asynchronous generator function to obtain a SQLAlchemy AsyncSession
    by calling the `create_session` function. It yields the session and
    ensures that the session is closed in case of an exception.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session.

    Note:
        This function is typically used as a dependency in FastAPI route
        handlers to provide a database session to the route. The session
        is closed in a `finally` block to ensure proper cleanup, especially
        in the presence of exceptions during the route processing.
    """
    session = await create_session()
    try:
        yield session
    except:
        session.close()
    finally:
        session.close()
