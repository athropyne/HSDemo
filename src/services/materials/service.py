from uuid import UUID

from aiohttp import ClientSession, FormData
from fastapi import Depends, UploadFile, HTTPException

from src.core.interfaces import BaseService
from src.services.materials.dto import MaterialAddInputModel, MaterialUpdateInputModel
from src.services.materials.repository import MaterialRepository


class MaterialService(BaseService):
    def __init__(self,
                 material_repository: MaterialRepository = Depends(MaterialRepository)):
        self.material_repository = material_repository

    async def create(self,
                     client_id: int,
                     file: UploadFile,
                     model: MaterialAddInputModel):
        # try:
        # Отправляем файл чанками во второй микросервис
        print(file.size)
        async with ClientSession() as session:
            # Создаем FormData для передачи файла
            data = FormData()
            data.add_field(
                "file",
                file.file,  # Используем file.file (SpooledTemporaryFile)
                filename=file.filename,
                content_type=file.content_type,
            )

            # Отправляем файл чанками
            async with session.post("http://localhost:10001/materials/", data=data) as response:
                print(response.status)
                if response.status != 201:
                    response_text = await response.text()
                    raise HTTPException(status_code=response.status, detail=response_text)

                return {"message": "File uploaded successfully"}
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=str(e))

        # if not file.filename.endswith(".svs"):
        #     raise HTTPException(status_code=400, detail="File must be a .svs file")
        # material_id = await self.material_repository.create(model.model_dump())
        #
        # # try:
        #     # Создаем временный файл
        # async with aiofiles.open('wb') as f:
        #     while chunk := await file.read(1024 * 1024):  # Читаем по 1 МБ
        #         await f.write(chunk)
        #     temp_file_path = f.name
        #
        # # Открываем файл .svs
        # slide = OpenSlide(temp_file_path)
        # slide_manager = SlideManager(slide)
        # start_time = datetime.datetime.now()
        # await slide_manager.save(material_id)
        # end_time = datetime.datetime.now()
        # print(f"Время сохранения: {end_time - start_time}")
        # buffer = io.BytesIO()
        # generator = DeepZoomGenerator(slide)

        # Обрабатываем и загружаем фрагменты

        # Закрываем слайд и удаляем временный файл
        # slide.close()
        # os.remove(temp_file_path)
        #
        # return JSONResponse(status_code=200, content={"message": "File processed and uploaded successfully"})
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=str(e))

    async def update(self,
                     client_id: int,
                     material_id: UUID,
                     model: MaterialUpdateInputModel):
        result = await self.material_repository.update(material_id, model.model_dump(exclude_none=True))
        return result

    async def get_list(self,
                       client_id: int,
                       case_id: int):
        ...

    # async def get_by_id(self,
    #                     client_id: int,
    #                     material_id: int):
    #     ...

    async def delete(self,
                     client_id: int,
                     material_id: UUID):
        ...
