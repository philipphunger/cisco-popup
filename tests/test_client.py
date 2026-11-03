import asyncio
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from xml.etree import ElementTree as ET

BASE = Path(__file__).resolve().parents[1] / 'custom_components/cisco_popup'
spec = importlib.util.spec_from_file_location('popup_client', BASE / 'client.py')
client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(client)
OK = b'<CiscoIPPhoneResponse><ResponseItem URL="" Data="Success" Status="0"/></CiscoIPPhoneResponse>'

class Response:
    status = 200
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
    async def read(self): return OK

class Session:
    def post(self, url, **kwargs):
        self.url, self.kwargs = url, kwargs
        return Response()

def run_immediate(coro):
    try:
        coro.send(None)
    except StopIteration:
        return
    raise AssertionError('Unexpected pending IO')

class Tests(unittest.TestCase):
    def test_escape_unicode(self):
        root = ET.fromstring(client.message_xml('Küche & Bad', '<fertig> 😀'))
        self.assertEqual(root.findtext('Title'), 'Küche & Bad')
        self.assertEqual(root.findtext('Text'), '<fertig> 😀')

    def test_invalid_controls(self):
        with self.assertRaises(client.PopupError): client.message_xml('Test', 'a\x00b')

    def test_phone_responses(self):
        client.check_response(200, OK)
        for status, raw in [(401, b''), (200, b'<html/>'), (200, b''),
                            (200, b'<CiscoIPPhoneResponse/>'),
                            (200, b'<CiscoIPPhoneResponse><ResponseItem Status="1"/></CiscoIPPhoneResponse>')]:
            with self.subTest(status=status, raw=raw), self.assertRaises(client.PopupError):
                client.check_response(status, raw)
        with self.assertRaisesRegex(client.PopupError, 'Authentifizierungs'):
            client.check_response(200, b'<CiscoIPPhoneError Number="4"/>')

    def test_post(self):
        session = Session()
        run_immediate(client.send_popup(session, '192.0.2.10', 'popup', 'popup', 'Test', 'Tür offen & Licht an'))
        self.assertEqual(session.url, 'http://192.0.2.10/CGI/Execute')
        self.assertFalse(session.kwargs['allow_redirects'])
        self.assertEqual(session.kwargs['auth'].login, 'popup')
        self.assertEqual(session.kwargs['auth'].password, 'popup')
        self.assertEqual(ET.fromstring(session.kwargs['data']['XML']).findtext('Text'), 'Tür offen & Licht an')

    def test_timeout(self):
        class TimeoutSession:
            def post(self, *args, **kwargs): raise asyncio.TimeoutError
        with self.assertRaisesRegex(client.PopupError, 'Zeitlimit'):
            run_immediate(client.send_popup(TimeoutSession(), '192.0.2.10', 'x', 'x', 'Test', 'Hallo'))

    def test_files(self):
        for file in BASE.glob('*.py'): compile(file.read_text(encoding='utf-8'), str(file), 'exec')
        manifest = json.loads((BASE / 'manifest.json').read_text())
        self.assertTrue(manifest['config_flow'])

if __name__ == '__main__': unittest.main(verbosity=2)
