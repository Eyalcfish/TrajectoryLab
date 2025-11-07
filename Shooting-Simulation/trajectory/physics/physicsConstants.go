package physics

import "shooting-simulator.com/shooting-simulator/utils/angle"

const (
	dt float64 = 0.01

	// TODO add buoyancy

	// * Ball constants:
	BallRadius         float64 = 0.12
	topWheelSpeedRatio float64 = 0.5
	omegaSpeedFactor   float64 = (1 - topWheelSpeedRatio) / (1 + topWheelSpeedRatio)

	crossSectionalArea float64 = angle.Pi * BallRadius * BallRadius
	ballMass           float64 = 0.27
	oneOverBallMass    float64 = 1 / ballMass

	// * Drag:
	dragCoefficient float64 = 0.55
	airDensity      float64 = 1.225

	airResistanceFactor float64 = 0.5 * dragCoefficient * airDensity * crossSectionalArea

	magnusFactor float64 = 0.5 * airDensity * crossSectionalArea * BallRadius * 0.25

	g float64 = 9.8

	ToleranceToDeclareAtStartOfTarget float64 = 0.05

	Inf float64 = 1e6

	// * Compression constants:
	// TODO Tune numbers
	ballInitialSpeedFromCompression float64 = 1.5
	compressionVelocityAngleOffset  float64 = -5 // * Degrees
)
