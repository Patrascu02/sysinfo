import time

durations = {}

def pytest_runtest_call(item):
    start = time.time()
    item.runtest()
    duration = time.time() - start
    durations[item.name] = duration

def pytest_sessionfinish(session, exitstatus):
    print("\n== ️Durata fiecarui test ==")
    for test_name, duration in durations.items():
        print(f"{test_name}: {duration:.4f} secunde")

