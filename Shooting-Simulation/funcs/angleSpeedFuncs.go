package funcs

func ShootingSpeed(dist float64, vel float64) float64 {
	speed := 0.0

	speed += 0.000265482 * dist * dist * dist
	speed += 0.00423254 * dist * dist * vel
	speed += -0.004902312 * dist * vel * vel
	speed += 0.001448454 * vel * vel * vel
	speed += -0.001901974 * dist * dist
	speed += 0.714083694 * dist
	speed += 0.061930493 * vel * vel
	speed += -0.195452625 * vel
	speed += -0.09052584 * dist * vel
	speed += 6.113945495

	return speed
}

func ShootingAngle(dist float64, vel float64) float64 {
	angle := 0.0

	angle += -0.000689976 * dist * dist * dist
	angle += 0.000703553 * dist * dist * vel
	angle += -0.000309973 * dist * vel * vel
	angle += -3.77314e-05 * vel * vel * vel
	angle += 0.014945124 * dist * dist
	angle += -0.156013787 * dist
	angle += 0.006145357 * vel * vel
	angle += 0.155159828 * vel
	angle += -0.016700097 * dist * vel
	angle += 1.475400899

	return angle
}
