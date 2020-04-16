import pyautogui
import math
import time

def calculate_distance(p1, p2):
	delta_x = p2.x - p1.x
	delta_y = p2.y - p1.y

	distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

	return distance

start_pos = pyautogui.position()
sleep_time = 0.001 # 1ms
while True:
	time.sleep(sleep_time)
	
	end_pos = pyautogui.position()
	dist = calculate_distance(start_pos, end_pos)
	velocity = dist / (1000 * sleep_time) # px / s
	if velocity != 0:
		print(f"Travelled at: {velocity} px / s")
	start_pos = end_pos