package main

import (
	"encoding/json"
	"fmt"
	"os"

	"shooting-simulator.com/shooting-simulator/constants"
	"shooting-simulator.com/shooting-simulator/export"
	"shooting-simulator.com/shooting-simulator/trajectory"
	"shooting-simulator.com/shooting-simulator/utils"
)

func main() {

	// settings import
	if len(os.Args) < 3 {
		fmt.Println("Usage: program <config.json> <output_file.csv>")
		return
	}

	configPath := os.Args[1]
	outputPath := os.Args[2]

	data, err := os.ReadFile(configPath)
	if err != nil {
		panic(err)
	}

	// temporary struct with pointers
	cfg := struct {
		TargetHeight               *float64 `json:"targetheight"`
		TargetRadius               *float64 `json:"targetradius"`
		DistanceTolerance          *float64 `json:"distancetolerance"`
		DTangential                *float64 `json:"dtangential"`
		DRadial                    *float64 `json:"dradial"`
		DRobotSpeed                *float64 `json:"drobotspeed"`
		MinHeightForMaxHeightCost  *float64 `json:"minheightformaxheightcost"`
		MaxHeightCostFactor        *float64 `json:"maxheightcostfactor"`
		MinDistance                *float64 `json:"mindistance"`
		MaxDistance                *float64 `json:"maxdistance"`
		DeltaDistance              *float64 `json:"deltadistance"`
		MinAngle                   *float64 `json:"minangle"`
		MaxAngle                   *float64 `json:"maxangle"`
		DeltaAngle                 *float64 `json:"deltaangle"`
		MinSpeed                   *float64 `json:"minspeed"`
		MaxSpeed                   *float64 `json:"maxspeed"`
		SpeedToleranceToStopSearch *float64 `json:"speedtolerancetostopsearch"`
		MaxRobotSpeed              *float64 `json:"maxrobotspeed"`
		DeltaRobotSpeed            *float64 `json:"deltarobotspeed"`
		ImpactVelocityCostWeight   *float64 `json:"impactvelocitycostweight"`
	}{}

	if err := json.Unmarshal(data, &cfg); err != nil {
		panic(err)
	}

	// helper function to override only if JSON provides value
	override := func(ptr *float64, target *float64) {
		if ptr != nil {
			*target = *ptr
		}
	}

	override(cfg.TargetHeight, &constants.TargetHeight)
	override(cfg.TargetRadius, &constants.TargetRadius)
	override(cfg.DistanceTolerance, &constants.DistanceTolerance)
	override(cfg.DTangential, &constants.DTangential)
	override(cfg.DRadial, &constants.DRadial)
	override(cfg.DRobotSpeed, &constants.DRobotSpeed)
	override(cfg.MinHeightForMaxHeightCost, &constants.MinHeightForMaxHeightCost)
	override(cfg.MaxHeightCostFactor, &constants.MaxHeightCostFactor)
	override(cfg.MinDistance, &constants.MinDistance)
	override(cfg.MaxDistance, &constants.MaxDistance)
	override(cfg.DeltaDistance, &constants.DeltaDistance)
	override(cfg.MinAngle, &constants.MinAngle)
	override(cfg.MaxAngle, &constants.MaxAngle)
	override(cfg.DeltaAngle, &constants.DeltaAngle)
	override(cfg.MinSpeed, &constants.MinSpeed)
	override(cfg.MaxSpeed, &constants.MaxSpeed)
	override(cfg.SpeedToleranceToStopSearch, &constants.SpeedToleranceToStopSearch)
	override(cfg.MaxRobotSpeed, &constants.MaxRobotSpeed)
	override(cfg.DeltaRobotSpeed, &constants.DeltaRobotSpeed)
	override(cfg.ImpactVelocityCostWeight, &constants.ImpactVelocityCostWeight)

	// main program
	var minCostShots []*trajectory.ShootingPoint

	for distanceToTarget := constants.MinDistance; distanceToTarget <= constants.MaxDistance; distanceToTarget += constants.DeltaDistance {

		percentageOfCalculation := 100 * (distanceToTarget - constants.MinDistance) / (constants.MaxDistance - constants.MinDistance)
		fmt.Println(utils.RoundToDecimal(percentageOfCalculation, 2), "%")

		for robotSpeed := -constants.MaxRobotSpeed; robotSpeed <= constants.MaxRobotSpeed; robotSpeed += constants.DeltaRobotSpeed {
			shotsOnTarget := trajectory.FindShotsOnTarget(distanceToTarget, robotSpeed)

			if len(shotsOnTarget) == 0 {
				continue
			}

			minCostShot := trajectory.MinimizeCost(shotsOnTarget)
			minCostShots = append(minCostShots, minCostShot)
		}
	}

	export.ExportData(minCostShots, outputPath)
	// fmt.Println("complete")
	// generateGraph(minCostShots)
	// http.ListenAndServe(":8081", nil)
}
