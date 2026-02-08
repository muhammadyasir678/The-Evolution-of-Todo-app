"""
Load testing script for Phase V services
This script simulates concurrent users performing various operations
"""

import asyncio
import aiohttp
import time
from typing import List, Dict
import random
import json


async def create_task(session: aiohttp.ClientSession, base_url: str, user_id: str, task_data: Dict):
    """Create a task for a user"""
    url = f"{base_url}/api/{user_id}/tasks"
    try:
        async with session.post(url, json=task_data) as response:
            result = await response.json()
            return response.status, result
    except Exception as e:
        return 500, {"error": str(e)}


async def get_tasks(session: aiohttp.ClientSession, base_url: str, user_id: str):
    """Get tasks for a user"""
    url = f"{base_url}/api/{user_id}/tasks"
    try:
        async with session.get(url) as response:
            result = await response.json()
            return response.status, result
    except Exception as e:
        return 500, {"error": str(e)}


async def update_task(session: aiohttp.ClientSession, base_url: str, user_id: str, task_id: int, update_data: Dict):
    """Update a task for a user"""
    url = f"{base_url}/api/{user_id}/tasks/{task_id}"
    try:
        async with session.put(url, json=update_data) as response:
            result = await response.json()
            return response.status, result
    except Exception as e:
        return 500, {"error": str(e)}


async def simulate_user_activity(session: aiohttp.ClientSession, base_url: str, user_id: str, num_operations: int):
    """Simulate a user performing various operations"""
    results = []
    
    for i in range(num_operations):
        # Randomly choose an operation
        operation = random.choice(["create", "get", "update"])
        
        if operation == "create":
            task_data = {
                "title": f"Load Test Task {i}",
                "description": f"Task created during load test #{i}",
                "completed": False,
                "priority": random.choice(["high", "medium", "low"]),
                "tags": random.sample(["work", "personal", "shopping", "urgent"], random.randint(1, 2)),
                "due_date": "2026-12-31T10:00:00Z" if random.random() > 0.5 else None,
                "recurrence_pattern": random.choice(["daily", "weekly", "monthly"]) if random.random() > 0.7 else None,
                "recurrence_interval": 1 if random.random() > 0.7 else None
            }
            status, result = await create_task(session, base_url, user_id, task_data)
            results.append(("create", status, result))
            
        elif operation == "get":
            status, result = await get_tasks(session, base_url, user_id)
            results.append(("get", status, result))
            
        elif operation == "update":
            # For update, we'll try to update a random task ID (some may fail, which is expected)
            task_id = random.randint(1, 1000)
            update_data = {
                "completed": random.choice([True, False]),
                "priority": random.choice(["high", "medium", "low"])
            }
            status, result = await update_task(session, base_url, user_id, task_id, update_data)
            results.append(("update", status, result))
    
    return results


async def run_load_test(base_url: str, num_users: int, operations_per_user: int):
    """Run the load test with specified parameters"""
    print(f"Starting load test with {num_users} users, {operations_per_user} operations per user...")
    print(f"Base URL: {base_url}")
    
    start_time = time.time()
    
    # Create an aiohttp session
    connector = aiohttp.TCPConnector(limit=100)  # Limit concurrent connections
    timeout = aiohttp.ClientTimeout(total=30)  # 30 second timeout
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # Create tasks for all users
        user_tasks = []
        for user_idx in range(num_users):
            user_id = f"user_{user_idx}"
            user_task = simulate_user_activity(session, base_url, user_id, operations_per_user)
            user_tasks.append(user_task)
        
        # Execute all user tasks concurrently
        all_results = await asyncio.gather(*user_tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Aggregate results
    total_ops = 0
    successful_ops = 0
    status_codes = {}
    
    for user_results in all_results:
        for op_type, status, result in user_results:
            total_ops += 1
            if status == 200 or status == 201:
                successful_ops += 1
            
            if status not in status_codes:
                status_codes[status] = 0
            status_codes[status] += 1
    
    # Print results
    print("\n--- LOAD TEST RESULTS ---")
    print(f"Total operations: {total_ops}")
    print(f"Successful operations: {successful_ops}")
    print(f"Success rate: {(successful_ops/total_ops)*100:.2f}%")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Operations per second: {total_ops/total_time:.2f}")
    print(f"Status codes: {status_codes}")
    
    # Performance metrics
    avg_response_time = total_time / total_ops if total_ops > 0 else 0
    print(f"Average response time: {avg_response_time:.3f} seconds")
    
    print("\n--- END RESULTS ---")


if __name__ == "__main__":
    # Configuration
    BASE_URL = "http://localhost:8000"  # Adjust to your backend URL
    NUM_USERS = 50  # Number of concurrent users
    OPERATIONS_PER_USER = 10  # Number of operations per user
    
    print("Load Testing Script for Phase V Services")
    print("="*50)
    
    # Run the load test
    asyncio.run(run_load_test(BASE_URL, NUM_USERS, OPERATIONS_PER_USER))