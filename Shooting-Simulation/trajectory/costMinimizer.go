package trajectory

import (
	"math"

	"shooting-simulator.com/shooting-simulator/constants"
	"shooting-simulator.com/shooting-simulator/utils"
	"shooting-simulator.com/shooting-simulator/utils/angle"
	"shooting-simulator.com/shooting-simulator/utils/vector"
)

func tangentialAddition(shot *ShootingPoint, shotVelocity *vector.Vector) *vector.Vector {
	tangentialAddition := vector.FromPolar(shot.Angle, constants.DTangential)
	shotVelocityWithTangentialChange := shotVelocity.Add(tangentialAddition)

	return shotVelocityWithTangentialChange
}

func radialAddition(shot *ShootingPoint, shotVelocity *vector.Vector) *vector.Vector {
	radialAddition := vector.FromPolar(shot.Angle+angle.HalfPi, constants.DRadial)
	shotVelocityWithRadialChange := shotVelocity.Add(radialAddition)

	return shotVelocityWithRadialChange
}

func robotSpeedAddition(shot *ShootingPoint) float64 {
	robotSpeedWithAddition := shot.RobotSpeed + constants.DRobotSpeed
	return robotSpeedWithAddition
}

func deltaDistance(shot *ShootingPoint, changedInitialVel *vector.Vector, changedRobotSpeed float64) float64 {
	shotDistanceWithChange, _, impactVelocity, _ := CalcTrajectory(
		changedInitialVel,
		changedRobotSpeed,
		constants.TargetHeight,
		math.Inf(1),
		0,
	)
	return (shotDistanceWithChange - shot.Distance) / impactVelocity.Angle()
}

func calcDistanceDerivative(shot *ShootingPoint) float64 {
	shotVelocity := vector.FromPolar(shot.Angle, shot.Speed)

	initialVelWithTangentialAddition := tangentialAddition(shot, shotVelocity)
	deltaDistanceWithTangentialChange := deltaDistance(shot, initialVelWithTangentialAddition, shot.RobotSpeed)
	distanceDerivativeTangential := deltaDistanceWithTangentialChange / constants.DTangential

	initialVelWithRadialAddition := radialAddition(shot, shotVelocity)
	deltaDistanceWithRadialChange := deltaDistance(shot, initialVelWithRadialAddition, shot.RobotSpeed)
	distanceDerivativeRadial := deltaDistanceWithRadialChange / constants.DRadial

	initialRobotSpeedWithChange := robotSpeedAddition(shot)
	deltaDistanceWithRobotSpeed := deltaDistance(shot, shotVelocity, initialRobotSpeedWithChange)
	distanceDerivativeRobotSpeed := deltaDistanceWithRobotSpeed / constants.DRobotSpeed

	distanceDerivative := utils.Hypot(
		distanceDerivativeTangential,
		distanceDerivativeRadial,
		distanceDerivativeRobotSpeed,
	)

	return distanceDerivative
}

func maxHeightCost(shot *ShootingPoint) float64 {
	if shot.MaxHeight < constants.MinHeightForMaxHeightCost {
		return 0
	}
	return constants.MaxHeightCostFactor * (shot.MaxHeight - constants.MinHeightForMaxHeightCost)
}

func calculateCost(shot *ShootingPoint) float64 {
	distanceDerivative := calcDistanceDerivative(shot)
	speedOfImpact := shot.velocityOfImpact.Norm()

	derivativeCost := math.Hypot(speedOfImpact*constants.ImpactVelocityCostWeight, distanceDerivative)
	maxHeightCost := maxHeightCost(shot)

	totalCost := derivativeCost + maxHeightCost
	return totalCost
}

func MinimizeCost(shots []*ShootingPoint) *ShootingPoint {
	minCost := math.Inf(1)
	var minCostShot *ShootingPoint

	for _, shot := range shots {
		cost := calculateCost(shot)

		if cost < minCost {
			minCost = cost
			minCostShot = shot
		}
	}

	return minCostShot
}
