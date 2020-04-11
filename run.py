import pyautogui
import time
from getkey import getkey
import random
import argparse

def setup_click_location():
	print(f"Setting up click location."
		f" Ensure this program remains in the computer's context."
		f" In other words, don't click away from this window."
		f"\n"
		f"Press any key when the mouse is in the correct position."
		)

	# blocks until keypress
	key_press = getkey()

	click_location = pyautogui.position()

	return click_location

def get_sleep_time():
	# sample from a gaussian distribution
	mu = 0.8
	sigma = 0.3
	return random.gauss(mu, sigma)

def continuously_click(click_location, runtime):
	print(f"Continously clicking for {runtime} minutes...")
	start = time.time()
	while True:
		if (time.time() - start) > runtime * 60:
			break

		random_time = get_sleep_time()
		print(f"Sleeping for {random_time}s.")
		time.sleep(random_time)
		
		print("Clicking!")
		pyautogui.click(click_location)

def run(runtime):
	click_location = setup_click_location()
	continuously_click(click_location, runtime)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--runtime', default=30, help='# of minutes to run for/', type=int)
	parsed = parser.parse_args()
	runtime = parsed.runtime
	
	run(runtime)
