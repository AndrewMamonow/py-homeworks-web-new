import asyncio
from aiohttp import ClientSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sw_loader import process_character, save_to_db

# Создаем подключение к базе данных
engine = create_async_engine('sqlite+aiosqlite:///star_wars.db')
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def main():
    # Получаем общее количество персонажей
    async with ClientSession() as session:
        base_url = 'https://swapi.info/api/people/'
        async with session.get(base_url) as response:
            data = await response.json()
            total_characters = len(data) #['count']
            # Формируем список URL для всех персонажей
            character_urls = [f'{base_url}{i}/' for i in range(1, total_characters + 1)]
        
        # Создаем задачи для обработки каждого персонажа
        tasks = []
        async with session:
            for url in character_urls:
                # Получаем данные персонажа
                character_data = await process_character(session, url)
                # Сохраняем данные в БД
                tasks.append(asyncio.create_task(save_to_db(AsyncSessionLocal, character_data)))
            
            # Ждем завершения всех задач
            await asyncio.gather(*tasks)
            print(f"Успешно загружено {total_characters} персонажей")

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Произошла ошибка: {e}")
