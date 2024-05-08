# main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pydantic import BaseModel
from database import get_database
from bson import ObjectId

# Khởi tạo FastAPI
app = FastAPI()

# Khởi tạo Jinja2Templates
templates = Jinja2Templates(directory="app/templates")


# Model Pydantic cho dữ liệu đầu vào
class Item(BaseModel):
    name: str
    age: int
    email: str  # Thêm trường email

# Route để hiển thị trang index.html
@app.get("/")
async def index1(request: Request):
    return templates.TemplateResponse("hienthi.html", {"request": request})

# Route để thêm dữ liệu
@app.post("/add_data/")
async def add_data(request: Request, item: Item):
    # Kết nối đến cơ sở dữ liệu
    db = await get_database()

    # Chọn collection "people"
    collection = db.people

    # Thêm dữ liệu vào collection
    result = collection.insert_one(item.dict())

    # Trả về id của document vừa được thêm
    return {"id": str(result.inserted_id)}

# Route để hiển thị tất cả dữ liệu
@app.get("/show_data/")
async def show_data(request: Request):
    # Kết nối đến cơ sở dữ liệu
    db = await get_database()

    # Chọn collection "people"
    collection = db.people

    # Lấy tất cả dữ liệu từ collection
    data = list(await collection.find().to_list(length=None))

    return templates.TemplateResponse("show_data.html", {"request": request, "data": data})

# Route để xóa dữ liệu bằng id
@app.post("/delete_data/")
async def delete_data(request: Request, id: str = Form(...)):
    # Kết nối đến cơ sở dữ liệu
    db = await get_database()

    # Chọn collection "people"
    collection = db.people

    # Xóa dữ liệu từ collection bằng id
    result = await collection.delete_one({"_id": ObjectId(id)})

    # Trả về kết quả của việc xóa
    if result.deleted_count == 1:
        message = f"Successfully deleted document with id {id}"
    else:
        message = f"Failed to delete document with id {id}"

    return {"message": message}

# Route để hiển thị trang delete.html
@app.get("/delete/")
async def delete(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1112)
