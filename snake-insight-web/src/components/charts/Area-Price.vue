<template>
  <div class="area-price" style="width: 100%;height: 40vh;"></div>
</template>

<script lang="ts" setup>
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: '天河'
  }
})
let region = toRef(props, 'region')
const options = reactive({
  title: {
    text: '天河区各地段平均价格'
  },
  tooltip: {},
  legend: {},
  dataset: {
    // 提供一份数据。
    source: [
      ['地段', '平均租房价格(元)'],
      ['越秀区', 5716.79],
      ['海珠区', 4559.26],
      ['天河区', 4541.14],
      ['白云区', 2980.35],
      ['黄埔区', 2879.66],
      ['番禺区', 3683.00],
      ['花都区', 2512.09],
      ['南沙区', 1939.32],
      ['增城区', 1929.85],
      ['从化区', 1939.32],
      ['荔湾区', 3566.63],
      ['广州周边',3453.74]
    ]
  },
  // 声明一个 X 轴，类目轴（category）。默认情况下，类目轴对应到 dataset 第一列。
  xAxis: { type: 'category',
    axisLabel: {
      color: '#333',
      //  让x轴文字方向为竖向
      interval: 0,
      formatter: function(value) {
        return value.split('').join('\n')
      }
    }},
  // 声明一个 Y 轴，数值轴。
  yAxis: {},
  // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
  series: [{ type: 'bar' }]
})
function  getDataSetSource() {
  // console.log(import.meta.env)
  // MESSAGE 传递Json格式数据要用POST方法
  $.post({
    url: import.meta.env.VITE_API_BASE_URL+'/plot',
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
      for (const plotDictKey in plotDict) {
        options.dataset.source.push([plotDictKey, plotDict[plotDictKey]])
      }
    }
  })
}
function initMap() {
  let avgPrice = echarts.init($('.area-price').get(0))
  avgPrice.showLoading()
  avgPrice.setOption(options)
  avgPrice.hideLoading()
  window.addEventListener('resize', () => {
    avgPrice.resize()
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