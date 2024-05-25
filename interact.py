class Interact(): 
    # Hàm kiểm tra va chạm
    def check_collision(rect1, rect2):
     if rect1.colliderect(rect2):
        intersection = rect1.clip(rect2)
        return (intersection.x, intersection.y)
     else:
        return None
     
