package plot

import (
	"net/http"

	"github.com/go-echarts/go-echarts/v2/charts"
	"github.com/go-echarts/go-echarts/v2/opts"
	"github.com/go-echarts/go-echarts/v2/types"
	"shooting-simulator.com/shooting-simulator/utils/vector"
)

func PlotScatter(data []*vector.Vector, title string) {
	http.HandleFunc("/"+title, func(w http.ResponseWriter, _ *http.Request) {
		scatter := charts.NewScatter()

		scatter.SetGlobalOptions(
			charts.WithInitializationOpts(opts.Initialization{Theme: types.ThemeRoma}),
			charts.WithTitleOpts(opts.Title{
				Title: title,
			}))

		chartDataPoints := []opts.ScatterData{}
		for _, dataPoint := range data {
			chartDataPoints = append(chartDataPoints, opts.ScatterData{Value: dataPoint.ToArray()})
		}

		scatter.AddSeries("", chartDataPoints)
		scatter.Render(w)
	})
}
