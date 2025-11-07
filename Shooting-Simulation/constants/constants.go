package constants

var (
	// * Target constants:
	TargetHeight      float64 = 2.2 // * relative shooter height
	TargetRadius      float64 = 0.2
	DistanceTolerance float64 = 0.01 // * meters on target

	// * Derivative deltas:c
	DTangential float64 = 1e-5
	DRadial     float64 = 1e-5
	DRobotSpeed float64 = 1e-5

	MinHeightForMaxHeightCost float64 = 2.8
	MaxHeightCostFactor       float64 = 0.125

	// * Calculation constants:
	MinDistance   float64 = 1 //min distance from robot to target
	MaxDistance   float64 = 4 //max distance from robot to target
	DeltaDistance float64 = 0.3//0.1

	MinAngle   float64 = 0 //min angle robot can get to
	MaxAngle   float64 = 90 // max angle robot can get to
	DeltaAngle float64 = 0.2

	MinSpeed                   float64 = 0 // min ball velocity
	MaxSpeed                   float64 = 25 // max ball velocity
	SpeedToleranceToStopSearch float64 = 1e-5

	MaxRobotSpeed   float64 = 3.2 // max robot speed
	DeltaRobotSpeed float64 = 0.38

	// * Cost calculation:
	ImpactVelocityCostWeight float64 = 0.3
)
