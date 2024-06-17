<template>
  <div :class="'floor-price' + has_elevator" style="width: 100%;height: 40vh;"></div>
</template>

<script lang="ts" setup>
let plot: any = null
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: '天河'
  },
  has_elevator: {
    type: Boolean,
    default: false
  }
})
const options = reactive({
  title: {
    text: `楼层(${props.has_elevator ? '有电梯' : '无电梯'})——每平方米价格`
  },
  tooltip: {},
  legend: {
    type: 'scroll',
    orient: 'vertical',
    right: 60,
    top: 30,
    bottom: 20

  },
  dataset: {
    // 提供一份数据。
    source: [

    ]
  },
  // 声明一个 X 轴，类目轴（category）。默认情况下，类目轴对应到 dataset 第一列。
  xAxis: {
    type: 'category',

  },
  // 声明一个 Y 轴，数值轴。
  yAxis: [
    {
      type: 'value',
      name: '价格(元)',
      position: 'left',
      axisLabel: {
        formatter: '{value}'
      }
    },
    {
      type: 'value',
      name: '统计数量',
      position: 'right',
      axisLabel: {
        formatter: '{value}'
      }
    }
  ],
  grid: {
    left: '2%',
    right: '2%',
    bottom: '12%',
    containLabel: true
  },
  // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
  series: [
    { type: 'line' },
    { type: 'line' },
    { type: 'line' },
    { type: 'bar', yAxisIndex: 1 }
  ]
})

function getDataSetSource() {
  // console.log(import.meta.env)
  // MESSAGE 传递Json格式数据要用POST方法
  $.post({
    url: import.meta.env.VITE_API_BASE_URL + '/getFloorPrice',
    // MESSAGE Json的编码格式
    contentType: 'application/json',
    async: true,
    // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
    data: JSON.stringify({
      "region": props.region,
      "require_elevator": props.has_elevator,
    }),
    success: (data: any) => {
      console.log(data)
      console.log(props.has_elevator)
      // MESSAGE 后端返回的格式并不按照SnachResponse的格式返回
      // MESSAGE 所以理论上不要用这个interface
      const plotDict = data.data
      const plotDictKeys = Object.keys(plotDict)
      const sortedKeys = plotDictKeys.sort((a, b) => Number(a) - Number(b))
      options.title.text = `${props.region}区 楼层(${props.has_elevator ? '有电梯' : '无电梯'})——每平方米价格`
      options.dataset.source = [['楼层', '每平方米最低价(元)', '平均每平方米价格(元)', '每平方米最高价(元)', '统计数量']]
      let width = 60
      for (const plotDictKey of sortedKeys) {
        let plotDictKeyNum = Number(plotDictKey)
        // console.log(plotDictKeyNum+' '+plotDict[plotDictKeyNum])
        options.dataset.source.push([plotDictKeyNum, plotDict[plotDictKeyNum][2], plotDict[plotDictKeyNum][0], plotDict[plotDictKeyNum][1], plotDict[plotDictKeyNum][3]])
        width += 25
      }
      let ratio = $('.floor-price' + props.has_elevator).width() / width
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
            bottom: 0
          },
          {
            type: 'inside',
            xAxisIndex: [0],
            start: 0,
            end: ratio * 100
          }
        ]
      }
      plot.setOption(options)
    }
  })
}

function initMap() {
  const elementName = '.floor-price' + props.has_elevator
  console.log(elementName)
  if (plot == null) {
    plot = echarts.init($(elementName).get(0))
  }
  plot.showLoading()
  plot.setOption(options)
  plot.hideLoading()
  window.addEventListener('resize', () => {
    plot.resize()
  })
}

watch(props, ()=>{
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