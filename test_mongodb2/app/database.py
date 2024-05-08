import os
import motor.motor_asyncio

async def get_database():
    # Kết nối đến MongoDB và chọn cơ sở dữ liệu "test"
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])
    db= client.myMongoDb
    collection = db.people

    return collection
