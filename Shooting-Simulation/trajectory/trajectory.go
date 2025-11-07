package trajectory

import (
	"math"

	"shooting-simulator.com/shooting-simulator/trajectory/physics"
	"shooting-simulator.com/shooting-simulator/utils"
	"shooting-simulator.com/shooting-simulator/utils/vector"
)

func CalcTrajectory(
	shotVelocity *vector.Vector,
	robotSpeed float64,
	targetHeight float64,
	distanceToTarget float64,
	targetRadius float64,
) (distance float64, maximumHeight float64, velocityOfImpact *vector.Vector, positions []*vector.Vector) {
	ballPosition := vector.Zero()

	robotSpeedVector := &vector.Vector{X: robotSpeed, Y: 0}
	ballInitialVelocityDueToCompression := physics.InitialVelocityFromCompression(shotVelocity)
	ballVelocity := shotVelocity.Add(robotSpeedVector).Add(ballInitialVelocityDueToCompression)

	distanceToStartOfTarget := distanceToTarget - targetRadius
	distanceToEndOfTarget := distanceToTarget + targetRadius

	prevAboveTarget := false

	omega := physics.CalcOmega(shotVelocity.Norm())
	maxHeight := 0.0

	var ballPositions []*vector.Vector

	for {
		ballPositions = append(ballPositions, ballPosition)

		aboveTarget := ballPosition.Y > targetHeight
		maxHeight = math.Max(ballPosition.Y, maxHeight)

		// * Check if ball entered target
		if prevAboveTarget && !aboveTarget {
			return ballPosition.X, float64(maxHeight), ballVelocity, ballPositions
		}

		// * Checking if ball can't go in at all
		goingDown := ballVelocity.Angle() < 0

		atStartOfTarget := utils.InTolerance(ballPosition.X, distanceToStartOfTarget, physics.ToleranceToDeclareAtStartOfTarget)
		hittingTarget := atStartOfTarget && ballPosition.Y < targetHeight+physics.BallRadius

		passedTarget := ballPosition.X > distanceToEndOfTarget
		notReachingTarget := goingDown && !aboveTarget

		if passedTarget {
			return physics.Inf, physics.Inf, vector.Zero(), []*vector.Vector{}
		}

		if notReachingTarget || hittingTarget {
			return -1, -1, vector.Zero(), []*vector.Vector{}
		}

		// * Update pos and vel
		ballVelocity = physics.CalcVelocity(ballVelocity, omega)
		ballPosition = physics.CalcPosition(ballPosition, ballVelocity)

		// * Update prev
		prevAboveTarget = aboveTarget
	}
}
