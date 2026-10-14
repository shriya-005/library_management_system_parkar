from services.member_service import(
    register_member,
    display_members,
    get_members
)
members = []

#register a new member
result = register_member(members, "M001", "Sanika")
print("Test 1:", result(["message"]))

#register another member
result = register_member(members, "M002", "Mrudula")
print("Test 2:", result(["message"]))

#reject duplicate ID
result = register_member(members, "M001", "Shriya")
print("Test 3:", result(["message"]))

#reject empty name
result = register_member(members, "M003", "")
print("Test 4:", result(["message"]))

#display all members
result = display_members(members)
print("Test 5:", result["data"])

#find an existing member
result = get_members(members, "M001")
print("Test 6:", result["message"])

#find non existent member
result = get_members(members, "M004")
print("Test 7:", result["message"])