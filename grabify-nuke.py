import sys
import time
import random
import requests
import threading

US_ONLY = True

messages = [
	"https://myg0t.win/",
	"https://myg0t.ru/",
	"myg0t owns u",
	"can you handle it, white boy?",
	"i have a massive PRICK",
	"Fuck white people #BlackLivesMatter",
	"i am a black trans woman",
	"i love COCKS in my ASSHOLE",
	"Black lives matter! #KillAllWhites #ACAB",
	"All whites are racist! #BLM",
	"White people are our slaves - myg0t.win",
	"I am a proud member of the LGBTQIAA+ community!",
	"I AM A GENDER BENDER TRANS RACIAL WOMAN",
	"myg0t - owning u since 1998",
	"HAHAHAHAHAHA - myg0t.win",
	"WE NEED A WHITE HOLOCAUST! #BLM",
	"FUCK ALL WHITE PIGS #ACAB #BLM",
	"AFRICAN WORMS ARE GETTING INTO OUR WHITE CHRISTIAN BLOOD STREAMS AND WE MUST STOP IT!!! https://myg0t.win/",
	"All cops are racist and white pigs! #ACAB #BlackLivesMatter",
	"BLACK LIVES MATTER YOU WHITE PIGS #KillAllWhites",
	"FUCK CHINK WORMS THEY ALL STINK AND STEAL OUR WHITE MONEY - myg0t.win",
]

def get_random_message():
	# Read our old message.
	cache_read = open(".cache", "r")
	old_status = str(cache_read.read())
	cache_read.close()

	# Select a random message to use.
	new_status = random.choice(messages)

	# Check if the message isn't the same as the old one.
	if new_status != old_status:
		# Save our new message to the cache.
		cache_write = open(".cache", "w")
		cache_write.write(new_status)
		cache_write.close()

		# Return our new message.
		return new_status
	else:
		# Recurse.
		return get_random_message()

def fetch_proxy_list():
	proxies = []

	data = requests.get("https://spys.me/proxy.txt")
	data_str = data.content.decode("utf-8")

	entries = data_str.split("\n")

	# first 9 lines can be trashed.
	for i in range(9):
		# we specify 0 because every time this loops the new array value will be 0.
		entries.pop(0)

	# last two lines can be trashed.
	for i in range(2):
		entries.pop(len(entries) - 1)

	# remove any bad listings.
	for entry in entries:
		if entry == "" or entry == "\r":
			continue

		try:
			addr, other, passed, space = entry.split(" ")
		except ValueError:
			continue

		# we only want successful proxies and ones that are in the states.
		if US_ONLY:
			if passed == "+" and other.startswith("US"):
				proxies.append(addr)
		else:
			if passed == "+":
				proxies.append(addr)

	return proxies

def thread_target(thread, url):
	try:
		proxy_addresses = fetch_proxy_list()

		for i in range(25):
			time.sleep(0.2)

			message = get_random_message()
			proxy_index = random.randint(0, len(proxy_addresses) - 1)

			try:
				proxy = {"http": proxy_addresses[proxy_index], "https": proxy_addresses[proxy_index]}

				requests.get(url, headers = { 'User-Agent': str(message) }, proxies = proxy)
				print(f"[{thread}] Sent request with User-Agent: \"{message}\" from {proxy_addresses[proxy_index]}")
			except TimeoutError:
				print(f"[{thread}] Connection timed out, retrying in 5 seconds...")
				time.sleep(5)
			except requests.exceptions.ProxyError:
				print(f"[{thread}] Connection with proxy timed out, removing \"{proxy_addresses[proxy_index]}\" from the proxy list...")

				# that proxy doesn't work, remove it from the list.
				proxy_addresses.pop(proxy_index)

	except Exception as e:
		print(f"[{thread}] An exception occured:\n{str(e)}")
		return

if __name__ == '__main__':
	try:
		print(f"[MAIN_THREAD] Creating threads...")

		# Create our threads.
		t1 = threading.Thread(target = thread_target, args = ("THREAD_1", sys.argv[1],))
		t2 = threading.Thread(target = thread_target, args = ("THREAD_2", sys.argv[1],))
		t3 = threading.Thread(target = thread_target, args = ("THREAD_3", sys.argv[1],))

		# Start up our threads.
		t1.start()
		t2.start()
		t3.start()

		# Wait for all threads to finish.
		t1.join()
		t2.join()
		t3.join()
	except IndexError:
		print("USAGE: python grabify-troll.py [GRABIFY URL]")
	except Exception as e:
		print(f"[MAIN_THREAD] Something fucked up: \n{str(e)}")
