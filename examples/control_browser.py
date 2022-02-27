# experimenting
# Could not get this to work yet.  Install errors on both Windows 10 and Raspberry Pi
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://joi-test-site.azurewebsites.net/')
    #await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
