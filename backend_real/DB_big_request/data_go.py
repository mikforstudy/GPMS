import httpx
import asyncio
import time

async def create_user(semaphore, session, user_data):
    async with semaphore:
        retries = 3
        for attempt in range(retries):
            try:
                response = await session.post("http://127.0.0.1:8000/api/v1/users/", json=user_data)
                if response.status_code == 200:
                    print(f"User {user_data['username']} created successfully")
                else:
                    print(f"Failed to create user {user_data['username']}: {response.text}")
                break
            except httpx.ReadTimeout:
                if attempt < retries - 1:
                    print(f"ReadTimeout occurred. Retrying {attempt + 1}/{retries}...")
                    await asyncio.sleep(1)
                else:
                    print(f"Failed to create user {user_data['username']} after {retries} attempts due to ReadTimeout")

async def main():
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
    timeout = httpx.Timeout(10.0, read=30.0)  # 设置超时时间
    semaphore = asyncio.Semaphore(100)  # 限制并发请求数量为100
    async with httpx.AsyncClient(limits=limits, timeout=timeout) as session:
        tasks = []
        for i in range(2000):
            user_data = {
                "username": f"user{i}",
                "password": "password123",
                "role": "student",
                "student_id": i,
                "teacher_id": 0
            }
            tasks.append(create_user(semaphore, session, user_data))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Runtime: {end_time - start_time} seconds")