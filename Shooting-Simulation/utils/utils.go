package utils

import "math"

func RoundToDecimal(x float64, decimalPlace int) float64 {
	tenToTheDecimal := math.Pow10(decimalPlace)
	return math.Round(float64(x*tenToTheDecimal)) / tenToTheDecimal
}

func InTolerance(value float64, wantedValue float64, tolerance float64) bool {
	return math.Abs(wantedValue-value) <= tolerance
}

func RoundToNearest(value float64, valueToNear float64, offset float64) float64 {
	// TODO log10 of value to near for round to decimal.
	return RoundToDecimal(math.Round((value-offset)/valueToNear)*valueToNear+offset, 2)
}

func Hypot(values ...float64) float64 {
	result := 0.0
	for _, value := range values {
		result += value * value
	}
	return math.Sqrt(result)
}
