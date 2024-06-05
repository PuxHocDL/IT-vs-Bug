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
    
    @staticmethod
    def collide_mask(mask1, mask2, pos1, pos2):
        return mask1.overlap(mask2, (pos2[0]-pos1[0], pos2[1]-pos1[1]))
    def collide_mask_2(mask1, mask2, pos1, pos2):
        return mask1.overlap(mask2, (pos2[0]-pos1[0], pos2[1]-pos1[1]))