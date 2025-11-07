package physics

import (
	"math"

	"shooting-simulator.com/shooting-simulator/utils/angle"
	"shooting-simulator.com/shooting-simulator/utils/vector"
)

func InitialVelocityFromCompression(shotVelocityWithoutCompression *vector.Vector) *vector.Vector {
	compressionVelocityAngle := angle.WrapAnglePlusMinusPi(shotVelocityWithoutCompression.Angle() + compressionVelocityAngleOffset)
	return vector.FromPolar(compressionVelocityAngle, ballInitialSpeedFromCompression)
}

func CalcOmega(linearSpeed float64) float64 {
	return omegaSpeedFactor * linearSpeed / BallRadius
}

func CalcPosition(prevPosition *vector.Vector, velocity *vector.Vector) *vector.Vector {
	return prevPosition.Add(velocity.Scale(dt))
}

func CalcVelocity(prevVelocity *vector.Vector, omega float64) *vector.Vector {
	dragForce := prevVelocity.Scale(-prevVelocity.Norm() * airResistanceFactor)

	magnusForceAngle := angle.WrapAnglePlusMinusPi(prevVelocity.Angle() + angle.HalfPi)
	magnusForceSize := prevVelocity.Norm() * math.Abs(omega) * magnusFactor

	magnusForce := vector.FromPolar(magnusForceAngle, magnusForceSize)

	var gravitationalForce *vector.Vector = &vector.Vector{X: 0, Y: -g * ballMass}

	totalForce := dragForce.Add(magnusForce).Add(gravitationalForce)
	totalAcceleration := totalForce.Scale(oneOverBallMass)

	return prevVelocity.Add(totalAcceleration.Scale(dt))
}
