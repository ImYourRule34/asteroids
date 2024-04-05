def check_collision(obj1, obj2):
  distance = ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2 ) ** .5
  return distance < (obj1.radius + obj2.radius)