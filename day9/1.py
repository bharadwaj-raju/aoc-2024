from util import readtext
from dataclasses import dataclass

diskmap = [int(x) for x in readtext().strip()]


@dataclass
class FileBlock:
    size: int
    id: int


@dataclass
class FreeBlock:
    size: int


type Block = FileBlock | FreeBlock

diskmap = [FileBlock(size, i // 2) if i % 2 == 0 else FreeBlock(size) for i, size in enumerate(diskmap)]

checksumkind = []
checksum = 0
ti = 0
for i, f in enumerate(diskmap):
    if isinstance(f, FileBlock) and f.size > 0:
        for _ in range(f.size):
            checksum += ti * f.id
            ti += 1
    else:
        try:
            replaced_f = next(
                block for block in reversed(diskmap[i:]) if isinstance(block, FileBlock) and block.size > 0
            )
            for _ in range(f.size):
                checksum += ti * replaced_f.id
                ti += 1
                replaced_f.size -= 1
                if replaced_f.size == 0:
                    replaced_f = next(
                        block for block in reversed(diskmap[i:]) if isinstance(block, FileBlock) and block.size > 0
                    )
        except StopIteration:
            break

print(checksum)
