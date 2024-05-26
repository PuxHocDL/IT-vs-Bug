class Interact(): 
    # Hàm kiểm tra va chạm
   def check_collision(rect1, rect2):
     if rect1.colliderect(rect2):
        intersection = rect1.clip(rect2)
        return (intersection.x, intersection.y)
     else:
        return None
     
   @staticmethod
   def check_collision_2(rect1, rect2):
        if rect1.colliderect(rect2):
            y_difference = abs(rect1.y - rect2.y)
            if y_difference <= 50:
                return True
        else:
            return False
       
     
