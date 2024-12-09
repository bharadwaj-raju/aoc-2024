from dataclasses import dataclass

from util import readtext

diskmap = [int(x) for x in readtext().strip()]


@dataclass
class FileBlock:
    size: int
    id: int


@dataclass
class FreeBlock:
    size: int


type Block = FileBlock | FreeBlock


def show_diskmap(diskmap):
    print("".join((str(x.id) * x.size) if isinstance(x, FileBlock) else ("." * x.size) for x in diskmap))


diskmap = [FileBlock(size, i // 2) if i % 2 == 0 else FreeBlock(size) for i, size in enumerate(diskmap)]

files_tail = len(diskmap) - 1
if files_tail % 2 != 0:
    files_tail -= 1

final = []
for i, f in enumerate(diskmap):
    if isinstance(f, FileBlock) and f.size > 0:
        final.extend(f.id for _ in range(f.size))
    else:
        try:
            if i > files_tail:
                break
            replaced_f = diskmap[files_tail]
            assert isinstance(replaced_f, FileBlock)
            for _ in range(f.size):
                final.append(replaced_f.id)
                replaced_f.size -= 1
                while replaced_f.size == 0:
                    files_tail -= 2
                    replaced_f = diskmap[files_tail]
                    assert isinstance(replaced_f, FileBlock)
                    if i > files_tail:
                        raise StopIteration
        except StopIteration:
            break

print(sum(i * x for i, x in enumerate(final)))
