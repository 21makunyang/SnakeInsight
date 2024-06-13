<template>
  <div class="area-price" style="width: 100%;height: 45vh;"></div>
</template>

<script lang="ts" setup>
let plot: any = null
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: '天河'
  }
})
const options = reactive({
  title: {
    text: '天河区各地段平均价格'
  },
  tooltip: {},
  legend: {
    type: 'scroll',
    orient: 'vertical',
    left: 10,
    top: 30,
    bottom: 20

  },
  dataset: {
    // 提供一份数据。
    source: [
      ['地段', '平均租房价格(元)'],

    ]
  },
  // 声明一个 X 轴，类目轴（category）。默认情况下，类目轴对应到 dataset 第一列。
  xAxis: {
    type: 'category',
    axisLabel: {
      color: '#333',
      //  让x轴文字方向为竖向
      interval: 0,
      formatter: function (value) {
        return value.split('').join('\n')
      }
    }
  },
  // 声明一个 Y 轴，数值轴。
  yAxis: {},
  grid: {
    left: '2%',
    right: '2%',
    bottom: '12%',
    containLabel: true
  },
  // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
  series: [{ type: 'bar' }],
})
function getDataSetSource() {
  // console.log(import.meta.env)
  // MESSAGE 传递Json格式数据要用POST方法
  $.post({
    url: import.meta.env.VITE_API_BASE_URL + '/plot',
    // MESSAGE Json的编码格式
    contentType: 'application/json',
    async: true,
    // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
    data: JSON.stringify({
      "loc": [`广州:${props.region}`],
      "x": "area",
      "ys": [["price", "Avg"]],
      "detailed": true
    }),
    success: (data: any) => {
      // MESSAGE 后端返回的格式并不按照SnachResponse的格式返回
      // MESSAGE 所以理论上不要用这个SnachResponse
      options.title.text = `${props.region}区各地段平均价格`
      const plotDict = data.plotData[0].value
      options.dataset.source = [['地段', '平均租房价格(元)']]
      let width = 60
      for (const plotDictKey in plotDict) {
        options.dataset.source.push([plotDictKey, plotDict[plotDictKey]])
        width += 25
      }
      let ratio = $('.area-price').width() / width
      console.log(ratio)
      if (ratio < 1) {
        options.dataZoom = [
          {
            type: 'slider',
            show: true,
            showDetail: false,
            xAxisIndex: [0],
            start: 0,
            end: ratio * 100,
            left: 'center',
            width: '75%',
            bottom: 40
          },
          {
            type: 'inside',
            xAxisIndex: [0],
            start: 0,
            end: ratio * 100
          }
        ]
      }
    }
  })
}
function initMap() {
  let plot = echarts.init($('.area-price').get(0))
  plot.showLoading()
  plot.setOption(options)
  plot.hideLoading()
  window.addEventListener('resize', () => {
    plot.resize()
  })
}
watch(options, () => {
  initMap()
})

onMounted(() => {
  setTimeout(() => {
    getDataSetSource()
    initMap()
  }, 20)
})
</script>