#!/usr/bin/python
# pylint: disable=missing-module-docstring
import sys
import os
import pynvim


def edit_file():
    """
    Editor file using neovim outside floating window.
    """

    socket_path = os.getenv('NVIM_LISTEN_ADDRESS')

    if not socket_path:
        sys.exit(1)

    client = pynvim.attach('socket', path=socket_path)

    try:
        pick_enable = client.vars['rnvimr_pick_enable']
    except KeyError:
        pick_enable = 0

    cmd = ['close'] if pick_enable else ['noautocmd wincmd p']

    for file in sys.argv[2:]:
        cmd.append('silent! edit {}'.format(file))

    if not pick_enable:
        cmd.append('noautocmd wincmd p')
        cmd.append('noautocmd startinsert')
    else:
        client.call('rnvimr#rpc#enable_attach_file', async_=True)

    client.command('|'.join(cmd), async_=True)


edit_file()
