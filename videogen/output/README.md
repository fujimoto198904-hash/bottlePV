# output/

生成物の一時置き場。Chrome操作（or 将来API）で作った成果物をここに、
`cli.py show <id>` が示す**厳密な出力名**で保存する:

- `base_kenji.png` / `base_manami.png` / `base_takashi.png`
- `still_SHOT01.png` … `still_SHOT09.png`
- `SHOT01_manami-order.mp4` … `SHOT09_manami-thanks.mp4`

`validate` / `faceguard` でチェックし、`set <id> approved` の後、`deliver` で
`bottle-scanner-video/domoai-exports/` へ納品する。ここのメディアは gitignore（納品先が正）。
