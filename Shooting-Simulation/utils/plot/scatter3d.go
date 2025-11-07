package plot

import (
	"math"
	"net/http"

	"github.com/go-echarts/go-echarts/v2/charts"
	"github.com/go-echarts/go-echarts/v2/opts"
)

var scatter3DColors = []string{
	"#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8",
	"#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026",
}

func convertToChartDataset(data [][]float64) ([]opts.Chart3DData, float64) {
	maxValue := math.Inf(-1)
	var chartDataSet []opts.Chart3DData
	for _, dataPoint := range data {
		var colorValue float64
		if len(dataPoint) > 3 {
			colorValue = dataPoint[3]
			maxValue = math.Max(maxValue, dataPoint[3])
		} else {
			colorValue = 0
			maxValue = math.Max(maxValue, dataPoint[2])
		}

		chartDataPoint := opts.Chart3DData{
			Value: []interface{}{dataPoint[0], dataPoint[1], dataPoint[2], colorValue},
		}
		chartDataSet = append(chartDataSet, chartDataPoint)
	}
	return chartDataSet, maxValue
}

func Scatter3D(chartTitle string, titles [4]string, data [][]float64) {
	http.HandleFunc("/"+chartTitle, func(w http.ResponseWriter, _ *http.Request) {
		chartDataset, maxValue := convertToChartDataset(data)

		line3d := charts.NewScatter3D()
		line3d.SetGlobalOptions(
			charts.WithVisualMapOpts(opts.VisualMap{
				Calculable: opts.Bool(true),
				Max:        float32(maxValue),
				InRange: &opts.VisualMapInRange{
					Color: scatter3DColors,
				},
				Text: []string{titles[3]},
			}),

			charts.WithGrid3DOpts(opts.Grid3D{
				ViewControl: &opts.ViewControl{
					AutoRotate:      opts.Bool(true),
					AutoRotateSpeed: 30,
				},
			}),
		)

		line3d.AddSeries("", chartDataset)

		line3d.XAxis3D.Name = titles[0]
		line3d.YAxis3D.Name = titles[1]
		line3d.ZAxis3D.Name = titles[2]
		line3d.Render(w)
	})
}
