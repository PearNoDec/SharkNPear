import sys
import threading
import asyncio
from asyncio import CancelledError
from mitmproxy import http
from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster
import chardet
import json
from PyQt6.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from utils.mitmaddon import MitmAddon

class SniffThread(QThread):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui

        self.running = False
        self.master = None
        self.loop = None
        self.stop_event = threading.Event()

    def run(self):
        self.running = True
        opts = Options(listen_port=self.gui.port)

        async def start_proxy():
            try:
                self.master = DumpMaster(opts, with_termlog=False, with_dumper=False)
                addons = [MitmAddon(self.gui)]
                self.master.addons.add(*addons)
                await self.master.run()
            except Exception as e:
                pass
                raise

        async def run_master():
            try:
                await start_proxy()
            except CancelledError:
                pass
            except Exception as e:
                pass
            finally:
                if self.master:
                    await self.master.shutdown()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(run_master())
        except Exception as e:
            pass
        finally:
            self.clean_up()

    def stop(self):
        self.running = False
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.cancel_all_tasks)
        if self.master:
            self.loop.call_soon_threadsafe(self.master.shutdown)
        self.stop_event.set()

    def cancel_all_tasks(self):
        for task in asyncio.all_tasks(self.loop):
            task.cancel()

    def clean_up(self):
        try:
            pending = asyncio.all_tasks(self.loop)
            for task in pending:
                task.cancel()
            self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
        except Exception as e:
            pass

    def wait(self, timeout=None):
        self.stop_event.wait(timeout)