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
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                
                log = []
                
                for i, step in enumerate(steps):
                    try:
                        result = self._execute_single_step(page, step, log)
                        if not result['success']:
                            browser.close()
                            return {
                                'success': False,
                                'error': result['error'],
                                'log': log,
                                'failed_step': i
                            }
                    except Exception as e:
                        browser.close()
                        return {
                            'success': False,
                            'error': f"Step {i} failed: {str(e)}",
                            'log': log,
                            'failed_step': i
                        }
                
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
        Execute a single automation step
        """
        action = step.get('action')
        description = step.get('description', f"Execute {action}")
        
        try:
            if action == 'goto':
                url = step.get('url')
                if not url:
                    return {'success': False, 'error': 'goto action requires url'}
                
                page.goto(url, wait_until='domcontentloaded')
                log.append(f"✓ Navigated to: {url}")
                return {'success': True}
            
            elif action == 'click':
                selector = step.get('selector')
                if not selector:
                    return {'success': False, 'error': 'click action requires selector'}
                
                # Wait for element to be visible and clickable
                page.wait_for_selector(selector, state='visible', timeout=10000)
                page.click(selector)
                log.append(f"✓ Clicked: {selector} - {description}")
                return {'success': True}
            
            elif action == 'type':
                selector = step.get('selector')
                text = step.get('text')
                if not selector or text is None:
                    return {'success': False, 'error': 'type action requires selector and text'}
                
                # Wait for element and clear before typing
                page.wait_for_selector(selector, state='visible', timeout=10000)
                page.fill(selector, text)
                log.append(f"✓ Typed '{text}' into: {selector} - {description}")
                return {'success': True}
            
            elif action == 'wait':
                selector = step.get('selector')
                timeout = step.get('timeout', 5000)
                
                if selector:
                    page.wait_for_selector(selector, state='visible', timeout=timeout)
                    log.append(f"✓ Waited for element: {selector}")
                else:
                    time.sleep(timeout / 1000)
                    log.append(f"✓ Waited for {timeout}ms")
                
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
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                page = await browser.new_page()
                
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