"""Read HIP counter/group metadata; never writes or extracts game assets."""
import argparse
import hashlib
import json
import struct
from pathlib import Path


def bkdr(name):
    value = 0
    for c in name.encode('ascii'):
        value = (value * 131 + c) & 0xFFFFFFFF
    return value


def inspect(path):
    data = path.read_bytes()
    if data[:8] != b'HIPA\0\0\0\0':
        raise ValueError('Expected HIPA header')
    assets = []

    def chunks(start, end):
        pos = start
        while pos < end:
            if end - pos < 8:
                raise ValueError('Truncated chunk header')
            tag, size = struct.unpack_from('>4sI', data, pos)
            payload, stop = pos + 8, pos + 8 + size
            if stop > end:
                raise ValueError('Chunk exceeds parent bounds')
            if tag in (b'DICT', b'ATOC'):
                chunks(payload, stop)
            elif tag == b'AHDR':
                if size < 36:
                    raise ValueError('Short asset header')
                aid, kind, off, length, plus, flags = struct.unpack_from('>I4sIIII', data, payload)
                if off + length > len(data):
                    raise ValueError('Asset exceeds archive bounds')
                if data[payload + 24:payload + 28] != b'ADBG':
                    raise ValueError('Missing asset debug metadata')
                dbgsize = struct.unpack_from('>I', data, payload + 28)[0]
                if payload + 32 + dbgsize != stop or dbgsize < 4:
                    raise ValueError('Invalid debug metadata bounds')
                name = data[payload + 36:stop].split(b'\0', 1)[0].decode('ascii', 'replace')
                assets.append({'id': f'0x{aid:08X}', 'type': kind.decode('ascii'),
                               'name': name, 'header_offset': pos,
                               'payload_offset': off, 'payload_size': length})
            pos = stop

    chunks(8, len(data))
    ids = [a['id'] for a in assets]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate asset IDs')
    wanted = {f'0x{bkdr(n):08X}' for n in
              ('PAUSESTATE MENU OR POWERUP COUNTER', 'PU SET TEXT ALL GROUP')}
    by_id = {a['id']: a for a in assets}
    selected = []
    for asset in assets:
        if asset['id'] not in wanted:
            continue
        item = dict(asset)
        off, size = item['payload_offset'], item['payload_size']
        if size < 8:
            raise ValueError('Short base asset')
        aid, basetype, links, flags = struct.unpack_from('<IBBH', data, off)
        if f'0x{aid:08X}' != item['id']:
            raise ValueError('Payload ID differs from header ID')
        item.update(base_type=basetype, link_count=links, base_flags=f'0x{flags:04X}')
        if item['type'] == 'CNTR':
            if size != 12 + links * 32:
                raise ValueError('Unexpected PS2 counter size')
            item['initial_count'] = struct.unpack_from('<h', data, off + 8)[0]
        elif item['type'] == 'GRUP':
            count, delegation = struct.unpack_from('<Hh', data, off + 8)
            if size != 12 + count * 4 + links * 32:
                raise ValueError('Unexpected PS2 group size')
            members = []
            for i in range(count):
                member = f'0x{struct.unpack_from("<I", data, off + 12 + i * 4)[0]:08X}'
                resolved = by_id.get(member)
                members.append({'id': member, 'name': resolved['name'] if resolved else None,
                                'type': resolved['type'] if resolved else None})
            item.update(item_count=count, delegation=delegation, members=members)
        selected.append(item)
    return {'archive': path.name, 'size': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'asset_headers_checked': len(assets), 'selected_assets': selected,
            'limits': 'Metadata only; no runtime event execution or cross-platform address mapping.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.archive), indent=2))
