package export

import (
	"io/fs"
	"os"
	"path"

	"golang.org/x/xerrors"
	"shooting-simulator.com/shooting-simulator/constants"
	"shooting-simulator.com/shooting-simulator/trajectory"
	"shooting-simulator.com/shooting-simulator/utils"
)

type outputDataPoint struct {
	Distance   float32 `csv:"distance"`
	Speed      float32 `csv:"speed"`
	RobotSpeed float32 `csv:"robot-speed"`
	Angle      float32 `csv:"angle"`
	MaxHeight  float32 `csv:"max-height"`
}

func ExportData(data []*trajectory.ShootingPoint, fileName string) error {
	var out []*outputDataPoint
	for _, point := range data {
		out = append(out, &outputDataPoint{
			Distance:   float32(utils.RoundToNearest(point.Distance, constants.DeltaDistance, constants.MinDistance)),
			Speed:      float32(point.Speed),
			RobotSpeed: float32(utils.RoundToNearest(point.RobotSpeed, constants.DeltaRobotSpeed, -constants.MaxRobotSpeed)),
			Angle:      float32(point.Angle),
			MaxHeight:  float32(point.MaxHeight),
		})
	}

	// Use the fileName as the full path, ensuring the directory exists.
	outputDirectory := path.Dir(fileName)
	if err := os.MkdirAll(outputDirectory, fs.ModePerm); err != nil {
		return xerrors.Errorf("error creating output directory: %w", err)
	}

	if err := saveCSV(fileName, &out); err != nil {
		return xerrors.Errorf("error in SaveCsv: %w", err)
	}

	return nil
}
