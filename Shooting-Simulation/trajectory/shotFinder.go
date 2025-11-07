package trajectory

import (
	"golang.org/x/xerrors"
	"shooting-simulator.com/shooting-simulator/constants"
	"shooting-simulator.com/shooting-simulator/utils"
	"shooting-simulator.com/shooting-simulator/utils/angle"
	"shooting-simulator.com/shooting-simulator/utils/vector"
)

func findSpeedForAngle(distanceToTarget float64, robotSpeed float64, angle float64) (*ShootingPoint, error) {
	minSpeedToSearch := constants.MinSpeed
	maxSpeedToSearch := constants.MaxSpeed
	for {
		speed := (minSpeedToSearch + maxSpeedToSearch) / 2

		shotVelocity := vector.FromPolar(angle, speed)

		calculatedDistance, maxHeight, velocityOfImpact, ballPositions := CalcTrajectory(
			shotVelocity,
			robotSpeed,
			constants.TargetHeight,
			distanceToTarget,
			constants.TargetRadius,
		)

		shootingPoint := &ShootingPoint{
			Angle:            angle,
			Speed:            speed,
			RobotSpeed:       robotSpeed,
			Distance:         calculatedDistance,
			MaxHeight:        maxHeight,
			velocityOfImpact: velocityOfImpact,
			Trajectory:       ballPositions,
		}

		inTarget := utils.InTolerance(shootingPoint.Distance, distanceToTarget, constants.DistanceTolerance)

		if inTarget {
			return shootingPoint, nil
		}

		if calculatedDistance < distanceToTarget {
			minSpeedToSearch = speed
		} else {
			maxSpeedToSearch = speed
		}

		if maxSpeedToSearch-minSpeedToSearch < constants.SpeedToleranceToStopSearch {
			return nil, xerrors.New("Couldn't find shot for given distance, robot speed and angle.")
		}
	}
}

func FindShotsOnTarget(distanceToTarget float64, robotSpeed float64) []*ShootingPoint {
	var shotsOnTarget []*ShootingPoint

	for angleDeg := constants.MinAngle; angleDeg <= constants.MaxAngle; angleDeg += constants.DeltaAngle {

		angleRad := angle.DegToRad(angleDeg)

		shot, err := findSpeedForAngle(distanceToTarget, robotSpeed, angleRad)
		if err != nil {
			continue
		}

		shotsOnTarget = append(shotsOnTarget, shot)
	}

	return shotsOnTarget
}
