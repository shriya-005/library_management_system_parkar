def register_member(members, member_id, name):
    member_id = member_id.strip()
    name = name.strip()

    if not member_id or not name:
        return{
            "success": False,
            "message": "Member ID and name cannot be empty",
            "data": None
        }

    for member in members:
        if member["member_id"]==member_id:
            return{
                "success": False,
                "message": "Member ID already exists.",
                "data": None
            }

    new_member={
        "member_id": member_id,
        "name": name,
        "borrowed_books":[]
    }
    members.append(new_member)

    return{
        "success": True,
        "message": "Member registered succesfully",
        "data": new_member
    }

def display_members(members):

    if not members:
        return{
            "success": True,
            "message": "No members registered yet.",
            "data": None
        }

    return{
        "success": True,
        "message": "Members retrived successfully",
        "data": members
    }

def get_members(members, member_id):

        member_id = member_id.strip()
        for member in members:
            if member["member_id"] == member_id:
                return{
                    "success": True,
                    "message": "Member found",
                    "data": member
                }

            return{
                "success": False,
                "message": "Member not found",
                "data": None
            }