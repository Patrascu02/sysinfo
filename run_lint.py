
import subprocess
import time

start = time.time()
result = subprocess.run(['pylint', 'lib'], capture_output=True, text=True)
end = time.time()

print(result.stdout)
print(f"\n==⏱️ Pylint a durat {end - start:.2f} secunde ==")
