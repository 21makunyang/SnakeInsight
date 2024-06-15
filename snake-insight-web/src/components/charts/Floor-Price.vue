<template>
  <div :class="'floor-price'+has_elevator" style="width: 100%;height: 40vh;"></div>
</template>

<script lang="ts" setup>
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: '天河'
  },
  has_elevator:{
    type: Boolean,
    default: false
  }
})
let region = toRef(props, 'region')
let avgPrice: any = null
const options = reactive({
  title: {
    text: `楼层(${props.has_elevator ? '有电梯' : '无电梯'})——每平方米价格`
  },
  tooltip: {},
  legend: {},
  dataset: {
    // 提供一份数据。
    source: [
      ['行政区', '平均租房价格(11元)'],
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
  xAxis: {
    type: 'category',

  },
  // 声明一个 Y 轴，数值轴。
  yAxis: {},
  // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
  series: [{ type: 'bar' }]
})

function getDataSetSource() {
  // console.log(import.meta.env)
  // MESSAGE 传递Json格式数据要用POST方法
  $.post({
    url: import.meta.env.VITE_API_BASE_URL+'/getFloorPrice',
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
      options.dataset.source = [['楼层', '平均每平方米价格(元)','每平方米最高价(元)','每平方米最低价(元)','统计数量']]
      for (const plotDictKey of sortedKeys) {
        let plotDictKeyNum = Number(plotDictKey)
        // console.log(plotDictKeyNum+' '+plotDict[plotDictKeyNum])
        options.dataset.source.push([plotDictKeyNum, plotDict[plotDictKeyNum][0], plotDict[plotDictKeyNum][1], plotDict[plotDictKeyNum][2], plotDict[plotDictKeyNum][3]])
      }
      avgPrice.setOption(options)
    }
  })
}

function initMap() {
  const elementName = '.floor-price'+props.has_elevator
  console.log(elementName)
  if(avgPrice == null) {
    avgPrice = echarts.init($(elementName).get(0))
  }
  avgPrice.showLoading()
  avgPrice.setOption(options)
  avgPrice.hideLoading()
  window.addEventListener('resize', () => {
    avgPrice.resize()
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