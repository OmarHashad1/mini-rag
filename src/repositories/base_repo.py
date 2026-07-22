from typing import Type
from beanie import Document
from typing import Optional
from pydantic import BaseModel


class BaseRepo:
    def __init__(self, model: Type[Document]):
        self.model = model

    async def insert_one(self, data: dict):
        document = self.model(**data)
        return await document.insert()

    async def insert_bulk(self, data: list, size: int = 10):
        documents_inserted = 0
        async with self.model.bulk_writer() as bulk:
            for i in range(0, len(data), size):
                batch = data[i : i + size]
                for item in batch:
                    document = self.model(**item)
                    await self.model.insert_one(document, bulk_writer=bulk)
                    documents_inserted += 1

        return documents_inserted

    async def insert_or_find_doc(self, data: dict):
        payload = await self.find_one(query=data)

        if payload is None:
            payload = await self.insert_one(data)

        return payload

    async def find_one(self, query: dict, projection: Optional[Type[BaseModel]] = None):
        return await self.model.find_one(query).project(projection_model=projection)

    async def find(self, query: dict, projection: Optional[Type[BaseModel]] = None):
        return (
            await self.model.find(query).project(projection_model=projection).to_list()
        )

    async def paginate(
        self,
        query: dict = {},
        projection: Optional[Type[BaseModel]] = None,
        page: int = 1,
        size: int = 10,
    ):
        documents_count = await self.model.find(query).count()
        total_pages = documents_count // size

        if documents_count % size > 0:
            total_pages = total_pages + 1

        docs = (
            await self.model.find(query)
            .project(projection_model=projection)
            .skip((page - 1) * size)
            .limit(size)
            .to_list()
        )

        metadata = {"page": page, "size": size, "total_pages": total_pages}
        return docs, metadata

    async def delete(self, query: dict):
        document = await self.model.find_one(query)
        if document is None:
            return None
        return await document.delete()

    async def delete_many(self, query: dict):
        return await self.model.find(query).delete()
