from ugit import data

print("HEAD resolves to:", data.get_ref("HEAD"))
print("testbranch resolves to:", data.get_ref("refs/heads/testbranch"))
print("Equal?", data.get_ref("HEAD") == data.get_ref("refs/heads/testbranch"))

