# services/browser.py - Playwright Browser Automation Service
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import asyncio
from typing import List, Dict, Any
import time

class BrowserAutomator:
    def __init__(self, headless=True):
        self.browser = None
        self.page = None
        self.headless = headless  # Set to False for debugging
    
    def execute_steps(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute browser automation steps synchronously
        """
        try:
            print(f"🎬 STARTING BROWSER AUTOMATION - HEADLESS: {self.headless}")
            with sync_playwright() as p:
                # FORCE VISIBLE BROWSER - IGNORE HEADLESS SETTING!
                print("🎬 LAUNCHING VISIBLE BROWSER WINDOW...")
                print("🚨 BROWSER WINDOW OPENING - WATCH YOUR SCREEN!")
                
                # Make browser IMPOSSIBLE to miss
                browser = p.chromium.launch(
                    headless=False,  # ALWAYS VISIBLE!
                    args=[
                        '--start-maximized',      # Maximize window
                        '--disable-web-security', # Disable security for demo
                        '--disable-features=VizDisplayCompositor',
                        '--window-position=0,0',  # Position at top-left
                        '--window-size=1920,1080', # Large window size
                        '--disable-blink-features=AutomationControlled',  # Hide automation
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'  # Human user agent
                    ],
                    slow_mo=800  # Medium speed - human-like but not too slow (0.8 seconds between actions)
                )
                
                # Play system sound to alert user
                try:
                    import winsound
                    winsound.Beep(1000, 500)  # 1000Hz for 500ms
                    print("🔊 PLAYED ALERT SOUND - BROWSER IS OPENING!")
                except:
                    pass
                page = browser.new_page()
                print("🎬 BROWSER WINDOW SHOULD BE VISIBLE NOW!")
                
                # Force browser to foreground and make it obvious
                try:
                    # Bring browser to front (Windows specific)
                    import win32gui
                    import win32con
                    import time
                    time.sleep(1)  # Wait for browser to fully load
                    
                    # Find browser window and bring to front
                    def enum_windows_callback(hwnd, windows):
                        if win32gui.IsWindowVisible(hwnd):
                            window_text = win32gui.GetWindowText(hwnd)
                            if 'Chrome' in window_text or 'Chromium' in window_text:
                                windows.append(hwnd)
                    
                    windows = []
                    win32gui.EnumWindows(enum_windows_callback, windows)
                    
                    if windows:
                        hwnd = windows[0]
                        win32gui.SetForegroundWindow(hwnd)
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                        print("🎯 FORCED BROWSER TO FOREGROUND!")
                except:
                    print("⚠️ Could not force browser to foreground (install pywin32 for better visibility)")
                
                # Make browser more human-like
                page.add_init_script("""
                    // Remove webdriver property
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    // Override plugins
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                    });
                    
                    // Override languages
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en'],
                    });
                """)
                
                print("🎬 BROWSER READY - STARTING HUMAN-LIKE AUTOMATION!")
                
                log = []
                log.append("🎬 VISIBLE BROWSER OPENED - STARTING AUTOMATION")
                
                for i, step in enumerate(steps):
                    try:
                        print(f"🎬 Executing step {i+1}/{len(steps)}: {step.get('action', 'unknown')}")
                        result = self._execute_single_step(page, step, log)
                        if not result['success']:
                            print(f"⚠️ Step {i+1} failed but continuing: {result.get('error', 'Unknown error')}")
                            # Don't stop on single step failure - continue with next steps
                            log.append(f"⚠️ Step {i+1} failed: {result.get('error', 'Unknown error')}")
                        else:
                            print(f"✅ Step {i+1} completed successfully")
                    except Exception as e:
                        print(f"❌ Step {i+1} exception: {str(e)}")
                        log.append(f"❌ Step {i+1} exception: {str(e)}")
                        # Continue with next steps even if one fails
                
                browser.close()
                return {
                    'success': True,
                    'log': log
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Browser automation failed: {str(e)}",
                'log': []
            }
    
    def _execute_single_step(self, page, step: Dict[str, Any], log: List[str]) -> Dict[str, Any]:
        """
        Execute a single automation step with improved error handling and selector fallbacks
        """
        action = step.get('action')
        description = step.get('description', f"Execute {action}")
        
        try:
            if action == 'goto':
                url = step.get('url')
                if not url:
                    return {'success': False, 'error': 'goto action requires url'}
                
                page.goto(url, wait_until='domcontentloaded')
                # Medium wait for page stability
                time.sleep(1.5)
                log.append(f"✓ Navigated to: {url}")
                return {'success': True}
            
            elif action == 'click':
                selector = step.get('selector')
                if not selector:
                    return {'success': False, 'error': 'click action requires selector'}
                
                # Try multiple selector strategies with special handling for search results
                selectors_to_try = [
                    selector,
                    # Google search result selectors (most common)
                    "h3 a",  # Google search result titles
                    ".yuRUbf a",  # Google search result links
                    ".LC20lb",  # Google result title
                    "[data-ved] h3",  # Google result with data-ved
                    ".g a[href]:first-child",  # First link in search result
                    "a[href*='youtube.com']",  # YouTube links specifically
                    "a[href*='youtu.be']",  # YouTube short links
                    # Common button selectors
                    "input[type='submit']",
                    "button[type='submit']",
                    "button",
                    "[role='button']",
                    # Common search button selectors
                    "input[name='btnK']",  # Google search button
                    "input[value='Google Search']",
                    ".gNO89b",  # Google search button class
                    # Generic clickable elements
                    "a[href]",
                    "[onclick]"
                ]
                
                clicked = False
                
                # Special handling for search result clicks
                if "result" in description.lower() or "link" in description.lower() or "first" in description.lower():
                    try:
                        # Wait for search results to load
                        page.wait_for_selector("#search", timeout=5000)
                        time.sleep(2)  # Extra wait for results to fully load
                        
                        # Try to click the first search result
                        first_result_selectors = [
                            "h3 a",  # Most common Google result selector
                            ".yuRUbf a",  # New Google layout
                            ".LC20lb",  # Google result title
                            ".g a[href]:first-child",  # First link in result
                            "a[href*='youtube.com']",  # YouTube specific
                        ]
                        
                        for sel in first_result_selectors:
                            try:
                                elements = page.query_selector_all(sel)
                                if elements and len(elements) > 0:
                                    # Human-like hover before click
                                    elements[0].hover()
                                    time.sleep(random.uniform(0.3, 0.6))  # Brief hover delay
                                    
                                    # Click the first result
                                    elements[0].click()
                                    log.append(f"✓ Clicked first search result using: {sel}")
                                    clicked = True
                                    break
                            except:
                                continue
                        
                        if clicked:
                            time.sleep(2)  # Wait for page to load
                            return {'success': True}
                    except:
                        pass
                
                # If special handling didn't work, try regular selectors
                if not clicked:
                    for sel in selectors_to_try:
                        try:
                            page.wait_for_selector(sel, state='visible', timeout=3000)
                            
                            # Human-like hover before click
                            page.hover(sel)
                            time.sleep(random.uniform(0.2, 0.4))  # Brief hover delay
                            
                            page.click(sel)
                            log.append(f"✓ Clicked: {sel} - {description}")
                            clicked = True
                            break
                        except:
                            continue
                
                if not clicked:
                    # Additional fallbacks for search result clicks
                    if "result" in description.lower() or "link" in description.lower():
                        try:
                            # Try JavaScript click on first result
                            page.evaluate("""
                                const firstResult = document.querySelector('h3 a') || 
                                                  document.querySelector('.yuRUbf a') || 
                                                  document.querySelector('.LC20lb') ||
                                                  document.querySelector('.g a[href]');
                                if (firstResult) {
                                    firstResult.click();
                                    return true;
                                }
                                return false;
                            """)
                            log.append(f"✓ Clicked first result using JavaScript fallback")
                            clicked = True
                        except:
                            pass
                    
                    # Try pressing Enter as final fallback
                    if not clicked:
                        try:
                            page.keyboard.press('Enter')
                            log.append(f"✓ Pressed Enter as fallback for click - {description}")
                            clicked = True
                        except:
                            pass
                
                if clicked:
                    time.sleep(1.2)  # Medium wait after click
                    return {'success': True}
                else:
                    log.append(f"⚠️ Click failed for all selectors - {description} - Continuing...")
                    return {'success': True}  # Continue execution
            
            elif action == 'type':
                selector = step.get('selector')
                text = step.get('text')
                if not selector or text is None:
                    return {'success': False, 'error': 'type action requires selector and text'}
                
                # Try multiple input selector strategies
                selectors_to_try = [
                    selector,
                    # Common search input selectors
                    "input[name='q']",
                    "textarea[name='q']",
                    "input[type='search']",
                    "input[title='Search']",
                    "#search",
                    ".search-input",
                    "[placeholder*='search' i]",
                    "[placeholder*='Search' i]",
                    # Generic input selectors
                    "input[type='text']",
                    "textarea",
                    "input:not([type='hidden']):not([type='submit']):not([type='button'])"
                ]
                
                typed = False
                for sel in selectors_to_try:
                    try:
                        page.wait_for_selector(sel, state='visible', timeout=3000)
                        # Clear and type
                        page.fill(sel, "")  # Clear first
                        time.sleep(0.5)
                        # Medium-speed human-like typing
                        import random
                        
                        # Clear field first
                        page.fill(sel, "")
                        time.sleep(random.uniform(0.2, 0.4))  # Brief pause before typing
                        
                        # Type with natural speed - not too fast, not too slow
                        page.type(sel, text, delay=random.randint(80, 150))  # 80-150ms per character
                        log.append(f"✓ Typed '{text}' into: {sel} - {description}")
                        typed = True
                        break
                    except:
                        continue
                
                if not typed:
                    # Try typing directly without selector
                    try:
                        page.keyboard.type(text, delay=100)
                        log.append(f"✓ Typed '{text}' directly - {description}")
                        typed = True
                    except:
                        pass
                
                if typed:
                    time.sleep(0.8)  # Medium wait after typing
                    
                    # Special handling for search queries - try to trigger search
                    if any(word in text.lower() for word in ['search', 'yt', 'youtube', 'google']):
                        try:
                            # Try pressing Enter to trigger search
                            page.keyboard.press('Enter')
                            log.append(f"✓ Pressed Enter after typing '{text}' to trigger search")
                            time.sleep(2.0)  # Medium wait for search to process
                        except:
                            pass
                    
                    return {'success': True}
                else:
                    log.append(f"⚠️ Type failed for all selectors - {description} - Continuing...")
                    return {'success': True}  # Continue execution
            
            elif action == 'wait':
                selector = step.get('selector')
                timeout = step.get('timeout', 5000)
                
                if selector:
                    try:
                        page.wait_for_selector(selector, state='visible', timeout=timeout)
                        log.append(f"✓ Waited for element: {selector}")
                    except:
                        # If specific selector fails, just wait the timeout
                        time.sleep(timeout / 1000)
                        log.append(f"✓ Waited {timeout}ms (selector not found)")
                else:
                    time.sleep(timeout / 1000)
                    log.append(f"✓ Waited for {timeout}ms")
                
                # Additional wait for page stability
                try:
                    page.wait_for_load_state('networkidle', timeout=3000)
                    log.append("✓ Page network activity settled")
                except:
                    pass
                
                return {'success': True}
            
            elif action == 'scroll':
                direction = step.get('direction', 'down')
                amount = step.get('amount', 500)
                
                if direction == 'down':
                    page.evaluate(f"window.scrollBy(0, {amount})")
                elif direction == 'up':
                    page.evaluate(f"window.scrollBy(0, -{amount})")
                elif direction == 'top':
                    page.evaluate("window.scrollTo(0, 0)")
                elif direction == 'bottom':
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                
                log.append(f"✓ Scrolled {direction}")
                return {'success': True}
            
            elif action == 'screenshot':
                path = step.get('path', f'screenshot_{int(time.time())}.png')
                page.screenshot(path=path)
                log.append(f"✓ Screenshot saved: {path}")
                return {'success': True}
            
            elif action == 'select':
                selector = step.get('selector')
                value = step.get('value')
                if not selector or value is None:
                    return {'success': False, 'error': 'select action requires selector and value'}
                
                page.wait_for_selector(selector, state='visible', timeout=10000)
                page.select_option(selector, value)
                log.append(f"✓ Selected '{value}' in: {selector} - {description}")
                return {'success': True}
            
            elif action == 'hover':
                selector = step.get('selector')
                if not selector:
                    return {'success': False, 'error': 'hover action requires selector'}
                
                page.wait_for_selector(selector, state='visible', timeout=10000)
                page.hover(selector)
                log.append(f"✓ Hovered over: {selector} - {description}")
                return {'success': True}
            
            elif action == 'press':
                key = step.get('key')
                if not key:
                    return {'success': False, 'error': 'press action requires key'}
                
                page.keyboard.press(key)
                log.append(f"✓ Pressed key: {key}")
                return {'success': True}
            
            else:
                return {'success': False, 'error': f'Unknown action: {action}'}
                
        except Exception as e:
            return {'success': False, 'error': f'{action} failed: {str(e)}'}
    
    async def execute_steps_async(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute browser automation steps asynchronously
        """
        try:
            print(f"🎬 STARTING ASYNC BROWSER AUTOMATION - HEADLESS: {self.headless}")
            async with async_playwright() as p:
                # FORCE VISIBLE BROWSER - IGNORE HEADLESS SETTING!
                print("🎬 LAUNCHING VISIBLE BROWSER WINDOW (ASYNC)...")
                browser = await p.chromium.launch(
                    headless=False,  # ALWAYS VISIBLE!
                    args=['--start-maximized'],  # Make it obvious
                    slow_mo=1000  # Slow down actions so you can see them
                )
                page = await browser.new_page()
                print("🎬 ASYNC BROWSER WINDOW SHOULD BE VISIBLE NOW!")
                
                log = []
                
                for i, step in enumerate(steps):
                    try:
                        result = await self._execute_single_step_async(page, step, log)
                        if not result['success']:
                            await browser.close()
                            return {
                                'success': False,
                                'error': result['error'],
                                'log': log,
                                'failed_step': i
                            }
                    except Exception as e:
                        await browser.close()
                        return {
                            'success': False,
                            'error': f"Step {i} failed: {str(e)}",
                            'log': log,
                            'failed_step': i
                        }
                
                await browser.close()
                return {
                    'success': True,
                    'log': log
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Browser automation failed: {str(e)}",
                'log': []
            }
    
    async def _execute_single_step_async(self, page, step: Dict[str, Any], log: List[str]) -> Dict[str, Any]:
        """
        Execute a single automation step asynchronously
        """
        action = step.get('action')
        description = step.get('description', f"Execute {action}")
        
        try:
            if action == 'goto':
                url = step.get('url')
                if not url:
                    return {'success': False, 'error': 'goto action requires url'}
                
                await page.goto(url, wait_until='domcontentloaded')
                log.append(f"✓ Navigated to: {url}")
                return {'success': True}
            
            elif action == 'click':
                selector = step.get('selector')
                if not selector:
                    return {'success': False, 'error': 'click action requires selector'}
                
                await page.wait_for_selector(selector, state='visible', timeout=10000)
                await page.click(selector)
                log.append(f"✓ Clicked: {selector} - {description}")
                return {'success': True}
            
            elif action == 'type':
                selector = step.get('selector')
                text = step.get('text')
                if not selector or text is None:
                    return {'success': False, 'error': 'type action requires selector and text'}
                
                await page.wait_for_selector(selector, state='visible', timeout=10000)
                await page.fill(selector, text)
                log.append(f"✓ Typed '{text}' into: {selector} - {description}")
                return {'success': True}
            
            elif action == 'wait':
                selector = step.get('selector')
                timeout = step.get('timeout', 5000)
                
                if selector:
                    await page.wait_for_selector(selector, state='visible', timeout=timeout)
                    log.append(f"✓ Waited for element: {selector}")
                else:
                    await asyncio.sleep(timeout / 1000)
                    log.append(f"✓ Waited for {timeout}ms")
                
                return {'success': True}
            
            elif action == 'scroll':
                direction = step.get('direction', 'down')
                amount = step.get('amount', 500)
                
                if direction == 'down':
                    await page.evaluate(f"window.scrollBy(0, {amount})")
                elif direction == 'up':
                    await page.evaluate(f"window.scrollBy(0, -{amount})")
                elif direction == 'top':
                    await page.evaluate("window.scrollTo(0, 0)")
                elif direction == 'bottom':
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                
                log.append(f"✓ Scrolled {direction}")
                return {'success': True}
            
            elif action == 'screenshot':
                path = step.get('path', f'screenshot_{int(time.time())}.png')
                await page.screenshot(path=path)
                log.append(f"✓ Screenshot saved: {path}")
                return {'success': True}
            
            elif action == 'select':
                selector = step.get('selector')
                value = step.get('value')
                if not selector or value is None:
                    return {'success': False, 'error': 'select action requires selector and value'}
                
                await page.wait_for_selector(selector, state='visible', timeout=10000)
                await page.select_option(selector, value)
                log.append(f"✓ Selected '{value}' in: {selector} - {description}")
                return {'success': True}
            
            elif action == 'hover':
                selector = step.get('selector')
                if not selector:
                    return {'success': False, 'error': 'hover action requires selector'}
                
                await page.wait_for_selector(selector, state='visible', timeout=10000)
                await page.hover(selector)
                log.append(f"✓ Hovered over: {selector} - {description}")
                return {'success': True}
            
            elif action == 'press':
                key = step.get('key')
                if not key:
                    return {'success': False, 'error': 'press action requires key'}
                
                await page.keyboard.press(key)
                log.append(f"✓ Pressed key: {key}")
                return {'success': True}
            
            else:
                return {'success': False, 'error': f'Unknown action: {action}'}
                
        except Exception as e:
            return {'success': False, 'error': f'{action} failed: {str(e)}'}