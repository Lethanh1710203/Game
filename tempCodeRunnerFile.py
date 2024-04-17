elif event.key == K_UP:
                speed += speed_change  # Tăng tốc độ từ từ
            elif event.key == K_DOWN:
                speed -= speed_change  # Giảm tốc độ từ từ
            if speed < 1:  # Đảm bảo tốc độ không nhỏ hơn 1
                speed = 1