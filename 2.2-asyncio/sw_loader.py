import asyncio
from aiohttp import ClientSession
from models import Character
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_json(session: ClientSession, url: str) -> Dict:
    # Делаем запрос к данным
    async with session.get(url) as response:
        return await response.json()

async def get_related_data(session: ClientSession, urls: List[str], key) -> List[str]:
    # Получаем связанные данные
    tasks = [fetch_json(session, url) for url in urls]
    results = await asyncio.gather(*tasks)
    return [result[key] for result in results]

async def process_character(session: ClientSession, character_url: str) -> Dict:
    # Получаем данные персонажей по url
    data = await fetch_json(session, character_url)
    
    # Заполняем связанные данные
    films = await get_related_data(session, data['films'], 'title')
    species = await get_related_data(session, data['species'], 'name')
    vehicles = await get_related_data(session, data['vehicles'], 'name')
    starships = await get_related_data(session, data['starships'], 'name')
    
    results = {
        'id': character_url.split('/')[-2],
        'birth_year': data.get('birth_year', ''),
        'eye_color': data.get('eye_color', ''),
        'films': ', '.join(films),
        'gender': data.get('gender', ''),
        'hair_color': data.get('hair_color', ''),
        'height': data.get('height', ''),
        'homeworld': data.get('homeworld', ''),
        'mass': data.get('mass', ''),
        'name': data.get('name', ''),
        'skin_color': data.get('skin_color', ''),
        'species': ', '.join(species),
        'starships': ', '.join(starships),
        'vehicles': ', '.join(vehicles)
    }
    return results

async def save_to_db(db_session: AsyncSession, character: Dict):
    # Заполняем данные для сохранения
    async with db_session() as session:
        async with session.begin():
            new_character = Character(
                id=character['id'],
                birth_year=character['birth_year'],
                eye_color=character['eye_color'],
                films=character['films'],
                gender=character['gender'],
                hair_color=character['hair_color'],
                height=character['height'],
                homeworld=character['homeworld'],
                mass=character['mass'],
                name=character['name'],
                skin_color=character['skin_color'],
                species=character['species'],
                starships=character['starships'],
                vehicles=character['vehicles'], )
    
    session.add(new_character) # добавляем данные в базу
    await session.commit() 