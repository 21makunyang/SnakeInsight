<template>
  <div class="space-price" style="width: 100%;height: 40vh;"></div>
</template>

<script lang="ts" setup>
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: ''
  }
})

let avgPrice: any = undefined
const region = toRef(props, 'region')
const options = reactive({
  title: {
    text: '面积——每平方米价格'
  },
  tooltip: {},
  legend: {
    type: 'scroll',
    right: 'right',
    orient: 'vertical',
    // left: 10,
    top: 30,
    bottom: 20
  },
  dataset: {
    // 提供一份数据。
    source: [['', 0]]
  },
  // 声明一个 X 轴，数值轴。默认情况下，每个系列会自动对应到 dataset 的每一列。
  xAxis: {type: 'value', name: '面积(m²)',},
  // 声明一个 Y 轴，数值轴。
  yAxis: {type: 'value', name: '价格(元)',},
  // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
  series: [{
    type: 'scatter',
    encode: { tooltip: [0, 1] },
    symbolSize: function (value) {
      return 3;
    }
  }]
})

function getDataSetSource() {
  $.post({
    url: import.meta.env.VITE_API_BASE_URL + '/plot',
    // MESSAGE Json的编码格式
    contentType: 'application/json',
    async: true,
    // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
    data: JSON.stringify({
      "loc": [`广州${props.region? `:` + props.region: ''}`],
      "x": "space",
      "ys": [["price", "Avg"]],
      "detailed": true
    }),
    success: (data: any) => {
      // MESSAGE 后端返回的格式并不按照SnachResponse的格式返回
      // MESSAGE 所以理论上不要用这个interface
      // console.log(data)
      if (props.region) {
        options.title.text = `${props.region}区 面积——每平方米价格`
      } else {
        options.title.text = `广州市 面积——每平方米价格`
      }
      const plotDict = data.plotData[0].value
      options.dataset.source = [['面积', '每平方米价格(元)']]
      // const plotDictKeys = Object.keys(plotDict)
      // const sortedKeys = plotDictKeys.sort((a, b) => Number(a) - Number(b))

      for (const plotDictKey in plotDict) {
        options.dataset.source.push([plotDictKey, (plotDict[plotDictKey] / Number(plotDictKey)).toFixed(2)])
      }

    }
  })
}

function initMap() {
  if (avgPrice === undefined) {
    avgPrice = echarts.init($('.space-price').get(0))
  }
  avgPrice.showLoading()
  avgPrice.setOption(options)
  avgPrice.hideLoading()
  window.addEventListener('resize', () => {
    avgPrice.resize()
  })
}

watch(props, () => {
  getDataSetSource()
})
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