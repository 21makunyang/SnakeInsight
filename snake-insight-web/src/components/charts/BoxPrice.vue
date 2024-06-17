<template>
  <div class="box-price" style="width: 100%;height: 80vh;"></div>
</template>

<script lang="ts" setup>
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: '天河'
  }
})
let boxPrice: any = undefined
let dataAxisTitle: string[] = []
const options = reactive({
  title: {
    text: `${props.region}区 各区域价格箱型图`
  },
  tooltip: {
    trigger: 'item',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {},
  dataset: [
    {
      source: [[0]]
    },
    {
      transform: {
        type: 'boxplot',
        config: {
          itemNameFormatter: function (params: any) {
            return dataAxisTitle[params.value]?.split('').join('\n')
          }
        }
      }
    },
    {
      fromDatasetIndex: 1,
      fromTransformResult: 1
    }
  ],
  // 声明一个 y 轴
  yAxis: {
    type: 'value',
    name: '价格(元)',
    splitArea: {
      show: true
    }
  },
  // 声明一个 x 轴
  xAxis: {
    type: 'category',
    boundaryGap: true,
    nameGap: 30,
    splitArea: {
      show: true
    },
    splitLine: {
      show: false
    }
  },
  series: [
    {
      name: '箱型图',
      type: 'boxplot',
      datasetIndex: 1
    },
    {
      name: '离群值',
      type: 'scatter',
      encode: {x: 0, y: 1},
      datasetIndex: 2
    }
  ],
  // 缩放
  dataZoom: [
    {
      type: 'inside'
    },
    {
      type: 'slider',
      yAxisIndex: [0]
    }
  ]
})

function getDataSetSource() {
  $.post({
    url: import.meta.env.VITE_API_BASE_URL + '/plot',
    contentType: 'application/json',
    async: true,
    data: JSON.stringify({
      "loc": [`广州:${props.region}`],
      "x": "area",
      "ys": [["price", "Raw", true]],
      "detailed": true
    }),
    success: (data: any) => {
      options.title.text = `${props.region}区 各区域价格箱型图`

      let plotData = data['plotData'][0]['value']
      console.log(plotData)
      options.dataset[0].source = []
      dataAxisTitle = []
      for (const point of plotData) {
        let x: string = point[0], y: Array<number> = point[1]
        dataAxisTitle.push(x)
        options.dataset[0].source.push(y)
      }
    }
  })
}

function initMap() {
  if (boxPrice === undefined) {
    boxPrice = echarts.init($('.box-price').get(0))
  }
  boxPrice.showLoading()
  boxPrice.setOption(options)
  boxPrice.hideLoading()
  window.addEventListener('resize', () => {
    boxPrice.resize()
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