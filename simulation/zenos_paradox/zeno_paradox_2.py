particle_a = [10, 0, 0]
particle_b = [0, 0, 0]

particle_a_speed = 1
particle_b_speed = 10
time = 0
for _ in range(100):
    print("Time: " + str(time) + "s")
    print("A Position: " + str(particle_a[0]) + "m")
    print("B Position: " + str(particle_b[0]) + "m")
    print()
    particle_b_time = (particle_a[0] - particle_b[0]) / particle_b_speed
    time += particle_b_time
    particle_b[0] = particle_a[0]

    particle_a[0] += particle_b_time * particle_a_speed
