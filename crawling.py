import os
import time
import colorama

def clear_screen():
    os.system('clear')  # For Linux/OS X

def display_banner():
    banner = """
---------------------------------------------------------------------------------------------------------------------
 _________    ___   _______           ______  _______          _  ____      ____  _____     ________  _______       |
|  _   _  | .'   `.|_   __ \        .' ___  ||_   __ \        / \|_  _|    |_  _||_   _|   |_   __  ||_   __ \      |
|_/ | | \_|/  .-.  \ | |__) |      / .'   \_|  | |__) |      / _ \ \ \  /\  / /    | |       | |_ \_|  | |__) |     |
    | |    | |   | | |  __ /       | |         |  __ /      / ___ \ \ \/  \/ /     | |   _   |  _| _   |  __ /      |
   _| |_   \  `-'  /_| |  \ \_     \ `.___.'\ _| |  \ \_  _/ /   \ \_\  /\  /     _| |__/ | _| |__/ | _| |  \ \_    |
  |_____|   `.___.'|____| |___|     `.____ .'|____| |___||____| |____|\/  \/     |________||________||____| |___|   |
------------------------------------------------------------------------------------------------------------------- |
                                                    
"""
    return banner

def animate_banner():
    clear_screen()
    banner = display_banner()
    colors = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE]
    color_index = 0
    for char in banner:
        print(colors[color_index % len(colors)] + char, end='', flush=True)
        time.sleep(0.01)  # Adjust the speed of typing effect
        color_index += 1
    print(colorama.Fore.RESET)  # Reset color after printing the banner

# Display the color cycling effect banner
animate_banner()



# Your existing code below
from urllib import response
import requests
from urllib.parse import urlparse, urljoin
from bs4 import *
import colorama
import os
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.traceback import install


# colorama module for basic ui 
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
BLUE = colorama.Fore.BLUE
YELLOW = colorama.Fore.YELLOW
CYAN = colorama.Fore.CYAN
RESET = colorama.Fore.RESET

# implementing TOR proxies
session = requests.session()
session.proxies["http"] = "socks5h://localhost:9050"
session.proxies["https"] = "socks5h://localhost:9050"

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()



table = Table(title="\n", style="white")

table.add_column("S.No", style="cyan")
table.add_column("Available Functions", style="bold italic", justify="center")

table.add_row("1.", "Crawling Internal endpoints")
table.add_row("2.", "Crawling Internal and External links")
table.add_row("3.", "Scraping web pages")
table.add_row("4.", "Downloading Images")
table.add_row("5.", "Exit from the Crawler")

console = Console()

# traceback design
install()



def crawl(url):

    response = session.get(url)
    urls = set()

    soup = BeautifulSoup(response.content, "html.parser")

    # title of the webpage
    print(f"{CYAN}\n[*] PAGE TITLE : ", soup.title.string)

    # get all the links on the webpage
    print(f"{YELLOW}\n[*] CRAWLED LINKS : \n")
    for link in soup.find_all("a"):
        # Need to change the content to crawl startswith. can include class name and xpath
        if link.get("href").startswith("/"):
            print(url + link.get("href"))
            urls.add(link)
        else:
            print(link.get("href"))
            urls.add(link)

    # extract text from the webpage
    # print(soup.get_text())

    print(f"{BLUE}\n[+] Total Crawled links:", len(urls))



def folder_create(images):
    try:
        folder_name = input("\nEnter Folder Name:- ")
        # folder creation
        os.mkdir(folder_name)

    # if folder exists with that name, ask another name
    except:
        print("\nFolder Exist with that name!")
        folder_create()

    # image downloading start
    download_images(images, folder_name)


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):

    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"\nTotal {len(images)} Image Found!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL

            # 1.data-srcset
            # 2.data-src
            # 3.data-fallback-src
            # 4.src

            # Here we will use exception handling

            # first we will search for "data-srcset" in img tag
            try:
                # In image tag ,searching for "data-srcset"
                image_link = image["data-srcset"]

            # then we will search for "data-src" in img
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag ,searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = image["src"]

                        # if no Source URL found
                        except:
                            pass

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                r = requests.get(image_link).content
                try:

                    # possibility of decode
                    r = str(r, 'utf-8')

                except UnicodeDecodeError:

                    # After checking above condition, Image Download start
                    with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                        f.write(r)

                    # counting number of image downloaded
                    count += 1
            except:
                pass

        if count == len(images):
            print("All Images Downloaded!")
        else:
            print(f"\nTotal {count} Images Downloaded Out of {len(images)}")


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    urls = set()
    response = session.get(url)
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(response.content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)

        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

# number of urls visited so far will be stored here
total_urls_visited = 0

def crawlInt(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawlInt(link, max_urls=max_urls)


def scraping(url): 

	response = session.get(url)
	
	soup = BeautifulSoup(response.content, "html.parser")

	# Extract title of page
	page_title = soup.title.text

	# Extract body of page
	page_body = soup.body

	# Extract head of page
	page_head = soup.head

	# print the result
	print(page_body)



console.print(table)

console.print("\nEnter an option to perform :", style="bold green")
opt = int(input())


while True:

	if opt == 1:
		console.print("\nEnter the URL :", style="bold sky_blue1")
		url=input()
		crawl(url)
		break

	elif opt == 2:
		max_urls=30
		console.print("\nEnter the URL :", style="bold sky_blue1")
		url=input()
		crawlInt(url)
		print("[+] Total Internal links:", len(internal_urls))
		print("[+] Total External links:", len(external_urls))
		print("[+] Total Crawled URLs:", len(external_urls) + len(internal_urls))
		break

	elif opt == 3:
		console.print("\nEnter the URL :", style="bold sky_blue1")
		url=input()
		scraping(url)
		break


	elif opt == 4:
		console.print("\nEnter the URL :", style="bold sky_blue1")
		url=input()
		r = session.get(url);

		# Parse HTML Code
		soup = BeautifulSoup(r.text, 'html.parser')

		# find all images in URL
		images = soup.findAll('img')

		# Call folder create function
		folder_create(images)
		break

	else:
		print("Exited")
		break
