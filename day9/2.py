from util import readtext
from dataclasses import dataclass

diskmap = [int(x) for x in readtext().strip()]


@dataclass
class FileBlock:
    size: int
    id: int
    moved: bool = False


@dataclass
class FreeBlock:
    size: int


type Block = FileBlock | FreeBlock

diskmap = [FileBlock(size, i // 2) if i % 2 == 0 else FreeBlock(size) for i, size in enumerate(diskmap)]

files = {f.id: f for f in diskmap if isinstance(f, FileBlock)}

for f_id in range(max(files), -1, -1):
    f = files[f_id]
    try:
        i_f = diskmap.index(f)
        i, leftmost_free = next(
            (i, b) for i, b in enumerate(diskmap) if isinstance(b, FreeBlock) and b.size >= f.size and i < i_f
        )
        diskmap[i_f] = FreeBlock(size=f.size)
        leftmost_free.size -= f.size
        del diskmap[i]
        diskmap[i:i] = [FileBlock(size=f.size, id=f.id), leftmost_free]
        f.size = 0
    except StopIteration:
        pass

final = []

for i, f in enumerate(diskmap):
    if isinstance(f, FileBlock) and f.size > 0:
        for _ in range(f.size):
            final.append(f.id)
    elif isinstance(f, FreeBlock):
        final.extend(0 for _ in range(f.size))

print(sum(i * x for i, x in enumerate(final)))
