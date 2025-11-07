package trajectory

import "shooting-simulator.com/shooting-simulator/utils/vector"

type ShootingPoint struct {
	Angle            float64
	Speed            float64
	RobotSpeed       float64
	Distance         float64
	MaxHeight        float64
	velocityOfImpact *vector.Vector
	Trajectory       []*vector.Vector
}
