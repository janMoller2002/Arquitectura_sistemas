import requests

BASE_URL = "http://localhost:5000"

def test_add_task_without_title():
    resp = requests.post(f"{BASE_URL}/api/tasks", json={})
    print("Test add_task_without_title:", resp.status_code, resp.json())

def test_add_task_with_title():
    resp = requests.post(f"{BASE_URL}/api/tasks", json={"title": "Tarea de prueba"})
    print("Test add_task_with_title:", resp.status_code, resp.json())

def test_complete_nonexistent_task():
    resp = requests.put(f"{BASE_URL}/api/tasks/999/complete")
    print("Test complete_nonexistent_task:", resp.status_code, resp.json())

def test_delete_nonexistent_task():
    resp = requests.delete(f"{BASE_URL}/api/tasks/999")
    print("Test delete_nonexistent_task:", resp.status_code, resp.json())

def test_simulate_error():
    resp = requests.post(f"{BASE_URL}/api/tasks/simulate-error")
    print("Test simulate_error:", resp.status_code, resp.json())

def test_error_stats():
    resp = requests.get(f"{BASE_URL}/errors/stats")
    print("Test error_stats:", resp.status_code, resp.json())

if __name__ == "__main__":
    test_add_task_without_title()
    test_add_task_with_title()
    test_complete_nonexistent_task()
    test_delete_nonexistent_task()
    test_simulate_error()
    test_error_stats()
