import requests
import asyncio
from pyppeteer import launch



# Function to convert HTML to PDF using headless Chrome
async def html_to_pdf(url, filename):
	browser = await launch()
	page = await browser.newPage()
	await page.goto(url)
	await page.pdf({'path': filename})
	await browser.close()


# Link:
url = input("Paste link here: ")


try:
	# Case 1: web is already a .pdf
	if url.lower().endswith(".pdf"):
		response = requests.get(url)

		if response.status_code == 200:
			filename = input("Enter how you want your file to be named: ")
			filename += ".pdf"
			with open(filename, "wb") as f:  # 'wb' = write binary (for files like PDFs)
				f.write(response.content)
				print(f"PDF downloaded as {filename}")


		else:
			print(f"Failed to download PDF. Status code: {response.status_code}")

	# Case 2: Otherwise, treat it as an HTML page and convert to PDF
	else:
		response = requests.get(url)

		if response.status_code == 200:
			filename = input("Enter how you want your file to be named: ")
			filename += ".pdf"
			import asyncio
			loop = asyncio.get_event_loop()  # Get the current event loop
			loop.run_until_complete(html_to_pdf(url, filename))  # Run your async function
			loop.close()  # Close the loop to avoid RuntimeError
			print(f"Webpage converted to PDF as {filename}")
			print(f"PDF downloaded as {filename}")

		else:
			print(f"Failed to load webpage. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
	print(f"Error: {e}")
