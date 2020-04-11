import pyautogui
import time
from getkey import getkey
import random
import argparse

CHANCE_TO_PERTURBATE_LOCATION = 0.015
CHANCE_TO_TAKE_BREAK = 0.003
CHANCE_TO_RANDOMLY_MOVE_MOUSE = 0.002

class ClickLocation:

	MARGIN_FOR_ERROR_PX = 3

	def __init__(self, original_location):
		'''
		original_location: input at the beginning of the script. should be centered on click item
		current_location: the script's current notion of the location
		'''
		self.original_location = original_location
		self.current_location = original_location

	def maybe_slightly_perturbate(self):
		'''
		perturbate location, but ensure it stays within a 
		margin for error of the original location
		'''		
		if random.random() >= CHANCE_TO_PERTURBATE_LOCATION:
			return
		
		print("Perturbating location...")

		original_x = self.original_location.x
		original_y = self.original_location.y

		lower_bound_x = original_x - self.MARGIN_FOR_ERROR_PX
		upper_bound_x = original_x + self.MARGIN_FOR_ERROR_PX
		new_x = random.randint(lower_bound_x, upper_bound_x)

		lower_bound_y = original_y - self.MARGIN_FOR_ERROR_PX
		upper_bound_y = original_y + self.MARGIN_FOR_ERROR_PX
		new_y = random.randint(lower_bound_y, upper_bound_y)

		self.current_location = pyautogui.Point(new_x, new_y)

	def get_current_loc(self):
		return self.current_location


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

	return ClickLocation(click_location)

def get_sleep_time():
	# distribution params
	mus = [0.8, 0.6, 1.1]
	sigmas = [0.2, 0.3, 0.4]

	# randomly select a distribution 
	mu = random.choice(mus)
	sigma = random.choice(sigmas)

	# simulate human taking a break
	mu_break = 45
	sigma_break = 10
	if random.random() < CHANCE_TO_TAKE_BREAK:
		print("Taking a (fake) break!")
		mu = mu_break
		sigma = sigma_break

	# ensure no negative values are sent back.
	return max(random.gauss(mu, sigma), 0)

def maybe_randomly_move_mouse(click_location):
	def _move_mouse_randomly():
		num_movements = random.randint(1,8)
		for _ in range(num_movements):
			x_distance_to_move = random.gauss(mu=0, sigma=200)
			y_distance_to_move = random.gauss(mu=0, sigma=200)
			pyautogui.move(x_distance_to_move, 
							y_distance_to_move,
							duration = random.gauss(1.5, 0.3),
							tween=pyautogui.easeInOutQuad)
	
	if random.random() < CHANCE_TO_RANDOMLY_MOVE_MOUSE:
		print("Moving mouse randomly...")
		_move_mouse_randomly()

		pyautogui.moveTo(click_location.get_current_loc(), duration = random.gauss(1.5, 0.3), tween=pyautogui.easeInOutQuad)
		# slowly return mouse to original click location

def continuously_click(click_location, runtime):
	print(f"Continously clicking for {runtime} minutes...")
	start = time.time()
	while True:
		if (time.time() - start) > runtime * 60:
			print("Finishing...")
			break

		random_time = get_sleep_time()
		print(f"Sleeping for {random_time}s.")
		time.sleep(random_time)

		maybe_randomly_move_mouse(click_location)
		
		click_location.maybe_slightly_perturbate()
		
		print("Clicking!")
		pyautogui.click(click_location.get_current_loc())

def run(runtime):
	click_location = setup_click_location()
	continuously_click(click_location, runtime)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--runtime', default=30, help='# of minutes to run for/', type=int)
	parsed = parser.parse_args()
	runtime = parsed.runtime
	
	run(runtime)
