from dataclasses import dataclass

from util import readtext, Node

diskmap = [int(x) for x in readtext().strip()]


@dataclass
class FileBlock:
    size: int
    id: int


@dataclass
class FreeBlock:
    size: int
    before: FileBlock | None = None


type Block = FileBlock | FreeBlock


diskmap = [FileBlock(size, i // 2) if i % 2 == 0 else FreeBlock(size) for i, size in enumerate(diskmap)]

files: dict[int, Node[FileBlock | FreeBlock]] = {}

head = Node(diskmap[0])
ins = head
first_file = head.x
assert isinstance(first_file, FileBlock)
files[first_file.id] = head
free_list = []
for block in diskmap[1:]:
    ins = ins.insert_after(block)
    if isinstance(block, FileBlock):
        free_list[-1].x.before = block
        files[block.id] = ins
    else:
        free_list.append(ins)


def show(head):
    final = []

    for f in head:
        f = f.x
        if isinstance(f, FileBlock) and f.size > 0:
            for _ in range(f.size):
                final.append(f.id)
        elif isinstance(f, FreeBlock):
            final.extend("." for _ in range(f.size))

    print("".join(map(str, final)))


for f_id in range(max(files), -1, -1):
    f = files[f_id]
    assert isinstance(f.x, FileBlock)
    try:
        leftmost_free = None
        for free in free_list:
            if free.x.before.id > f.x.id:
                raise StopIteration
            if free.x.size >= f.x.size:
                leftmost_free = free
                break
        if leftmost_free is None:
            raise StopIteration

        leftmost_free.x.size -= f.x.size
        leftmost_free.insert_before(f.x)
        if leftmost_free.x.size == 0:
            leftmost_free.remove()
        f.x = FreeBlock(size=f.x.size)
    except StopIteration:
        pass
    free_list = [f for f in free_list if f.x.size > 0]

final = []

for f in head:
    f = f.x
    if isinstance(f, FileBlock) and f.size > 0:
        for _ in range(f.size):
            final.append(f.id)
    elif isinstance(f, FreeBlock):
        final.extend(0 for _ in range(f.size))

print(sum(i * x for i, x in enumerate(final)))
