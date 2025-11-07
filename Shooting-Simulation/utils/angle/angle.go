package angle

import "math"

const Pi = math.Pi
const HalfPi = math.Pi / 2
const TwoPi = math.Pi * 2

func DegToRad(angle float64) float64 {
	return angle * Pi / 180
}

func RadToDeg(angle float64) float64 {
	return angle * 180 / Pi
}

func WrapAnglePlusMinusPi(angle float64) float64 {
	// Getting the angle smallest form (not exceeding a full turn).
	wrapped := math.Mod(angle, TwoPi)

	// Adding or subtracting two pi to fit the range of +/- pi.
	if wrapped > Pi {
		return wrapped - TwoPi
	} else if wrapped < -Pi {
		return wrapped + TwoPi
	} else {
		return wrapped
	}
}
