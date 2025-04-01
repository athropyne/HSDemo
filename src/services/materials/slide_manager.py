import asyncio
import io

from loguru import logger
from openslide import AbstractSlide
from openslide.deepzoom import DeepZoomGenerator

from src.core.infrastructures import s3_client


class SlideManager:
    def __init__(self,
                 slide: AbstractSlide):
        self.slide = slide
        self.generator = DeepZoomGenerator(slide, tile_size=1022)
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=10)
        self.tile_count = self.generator.tile_count

    async def generate_tiles(self, prefix: str):
        for level_num, address in enumerate(self.generator.level_tiles):
            for column in range(address[0]):
                for row in range(address[1]):
                    tile = self.generator.get_tile(level_num, (column, row))
                    buffer = io.BytesIO()  # Новый буфер для каждого тайла
                    tile.save(buffer, format="JPEG")
                    buffer.seek(0)
                    tile_name = f"{prefix}/{level_num}_{column}_{row}.jpg"
                    # logger.debug(f"Попытка сохранения плитки {tile_name}")
                    await self.queue.put((tile_name, buffer))
                    # result = await s3_client.upload(tile_name, buffer, "image/jpeg")
                    # logger.debug(f"задача сохранения {tile_name} добавлена")
                    logger.debug(f"количество элементов в очереди {self.queue.qsize()}")

    async def worker(self):
        while True:
            tile_name, buffer = await self.queue.get()
            # logger.debug(f"задача {tile_name} принята")

            logger.debug(f"количество элементов в очереди {self.queue.qsize()}")
            if tile_name is None:  # Сигнал завершения
                break
            result = await s3_client.upload(tile_name, buffer, "image/jpeg")
            logger.info(f"Файл {tile_name} загружен")
            self.queue.task_done()
            self.tile_count -= 1
            logger.debug(f"файлов осталось {self.tile_count}")
            # logger.debug(f"задача сохранения {tile_name} выполнена")

    async def save(self, prefix: str, num_workers: int = 5):
        # Запускаем worker'ов
        workers = [asyncio.create_task(self.worker()) for _ in range(num_workers)]
        await self.generate_tiles(prefix)  # Генерируем тайлы
        await self.queue.join()  # Ждем завершения всех задач# Останавливаем worker'ов
        for _ in range(num_workers):
            await self.queue.put((None, None))  # Сигнал завершения
        await asyncio.gather(*workers)  # Ждем завершения worker'а

