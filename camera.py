def world_to_view(cam, grpMon):
    for i in grpMon:
        i.rect.x = i.rect.x - cam[0]
        i.rect.y = i.rect.y - cam[1]

def view_to_world(cam, grpMon):
    for i in grpMon:
        i.rect.x = i.rect.x + cam[0]
        i.rect.y = i.rect.y + cam[1]
