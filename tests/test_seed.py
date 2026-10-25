import unittest

from mcdreforged.api.all import Info, InfoSource
from mcdreforged.handler.impl.vanilla_handler import VanillaHandler

import seed


class SeedOutputTests(unittest.TestCase):
    def setUp(self):
        self.previous_state = seed.getting_seed, seed.seed, seed.config
        seed.getting_seed = True
        seed.seed = None
        # Existing installations retain this configuration after an upgrade.
        seed.config = {'command': 'seed', 'parser': 'Seed: [{}]'}

    def tearDown(self):
        seed.getting_seed, seed.seed, seed.config = self.previous_state

    def receive(self, content):
        info = Info(InfoSource.SERVER, content, content=content)
        seed.on_info(None, info)

    def test_minecraft_26_3_output_reported_by_user(self):
        self.receive('System chat: Seed: [6787745258450122489]')
        self.assertEqual(seed.seed, '6787745258450122489')

    def test_old_and_new_formats_preserve_seed_values(self):
        for prefix in ('', 'System chat: '):
            for value in ('0', '-12345', '-9223372036854775808', '9223372036854775807'):
                with self.subTest(prefix=prefix, value=value):
                    seed.seed = None
                    self.receive('{}Seed: [{}]'.format(prefix, value))
                    self.assertEqual(seed.seed, value)

    def test_real_mcdr_handler_then_plugin(self):
        info = VanillaHandler().parse_server_stdout(
            '[12:34:56] [Server thread/INFO]: System chat: Seed: [6787745258450122489]'
        )
        seed.on_info(None, info)
        self.assertEqual(seed.seed, '6787745258450122489')

    def test_custom_parser_with_old_and_new_output(self):
        seed.config['parser'] = 'World seed = {}'
        for prefix in ('', 'System chat: '):
            with self.subTest(prefix=prefix):
                seed.seed = None
                self.receive(prefix + 'World seed = -42')
                self.assertEqual(seed.seed, '-42')

    def test_custom_parser_including_system_chat_prefix(self):
        seed.config['parser'] = 'System chat: Seed: [{}]'
        self.receive('System chat: Seed: [42]')
        self.assertEqual(seed.seed, '42')

    def test_explicit_custom_parser_takes_priority(self):
        seed.config['parser'] = '{}'
        self.receive('System chat: custom output')
        self.assertEqual(seed.seed, 'System chat: custom output')

    def test_unrelated_output_is_ignored(self):
        for content in (
            'System chat: Preparing spawn area: 10%',
            '<Player> System chat: Seed: [42]',
            'Some log mentions System chat: Seed: [42]',
            'System chat: Seed: [42] extra text',
        ):
            with self.subTest(content=content):
                self.receive(content)
                self.assertIsNone(seed.seed)

    def test_output_is_ignored_when_not_getting_seed(self):
        seed.getting_seed = False
        self.receive('System chat: Seed: [42]')
        self.assertIsNone(seed.seed)


if __name__ == '__main__':
    unittest.main()
